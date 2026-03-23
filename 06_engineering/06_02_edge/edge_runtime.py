from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

from edge_adapter_protocol import EdgeAdapterProtocol
from edge_heartbeat import LinkSupervisor
from edge_models import EdgeCommand, EdgeCommandType, EdgeRecord, EdgeRuntimeSnapshot
from edge_runtime_config import DEFAULT_EDGE_RUNTIME_CONFIG, EdgeRuntimeConfig


def _load_module(module_name: str, module_path: Path) -> Any:
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module {module_name} from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _load_twin_domain_bundle() -> dict[str, Any]:
    twin_dir = Path(__file__).resolve().parents[1] / "06_01_sim_twin"
    models_module = _load_module("twin_models", twin_dir / "twin_models.py")
    publishers_module = _load_module("twin_publishers", twin_dir / "twin_publishers.py")
    state_machine_module = _load_module("twin_state_machine", twin_dir / "twin_state_machine.py")
    return {
        "TwinContext": models_module.TwinContext,
        "TwinEvent": models_module.TwinEvent,
        "TwinEventType": models_module.TwinEventType,
        "TwinStateMachine": state_machine_module.TwinStateMachine,
        "PublishedMessage": models_module.PublishedMessage,
        "InMemoryPublisher": publishers_module.InMemoryPublisher,
    }


class InMemoryEdgeAdapter:
    def __init__(self) -> None:
        self.records: list[EdgeRecord] = []

    def publish(self, record: EdgeRecord) -> None:
        self.records.append(record)
        print(
            f"[edge-record] kind={record.kind} state={record.state} "
            f"accepted={record.accepted} summary={record.summary} payload={record.payload}"
        )


class _EdgePublisherBridge:
    def __init__(self, adapter: EdgeAdapterProtocol) -> None:
        self.adapter = adapter
        self.messages: list[dict[str, Any]] = []

    def _publish(self, kind: str, context: Any, event: Any, **payload: Any) -> None:
        record = EdgeRecord(
            kind=kind,
            state=context.state.value,
            accepted=payload.get("result") == "accepted" if "result" in payload else None,
            summary=event.event_type.value,
            payload=payload,
            source="edge",
            corr_id=event.corr_id,
        )
        self.messages.append({"kind": kind, "state": context.state.value, "payload": payload})
        self.adapter.publish(record)

    def publish_status(self, context: Any, event: Any) -> None:
        self._publish(
            "status",
            context,
            event,
            prev_state=context.previous_state.value if context.previous_state else None,
            transition_reason=context.last_reason,
            traction_enabled=context.traction_enabled,
        )

    def publish_audit(self, context: Any, event: Any, result: str, reason: str) -> None:
        self._publish(
            "audit",
            context,
            event,
            result=result,
            reason=reason,
            event_type=event.event_type.value,
        )

    def publish_alarm(self, context: Any, event: Any, reason: str) -> None:
        self._publish("alarm", context, event, reason=reason)

    def publish_fault(self, context: Any, event: Any, reason: str) -> None:
        self._publish("fault", context, event, reason=reason)

    def publish_heartbeat(self, context: Any, event: Any, link_ok: bool) -> None:
        self._publish("heartbeat", context, event, link_ok=link_ok)

    def publish_telemetry(self, context: Any, event: Any, **telemetry: Any) -> None:
        self._publish("telemetry", context, event, **telemetry)


class EdgeRuntime:
    def __init__(
        self,
        adapter: EdgeAdapterProtocol | None = None,
        config: EdgeRuntimeConfig | None = None,
    ) -> None:
        self.adapter = adapter or InMemoryEdgeAdapter()
        self.config = config or DEFAULT_EDGE_RUNTIME_CONFIG
        bundle = _load_twin_domain_bundle()
        self._TwinEvent = bundle["TwinEvent"]
        self._TwinEventType = bundle["TwinEventType"]
        self.context = bundle["TwinContext"]()
        self.publisher = _EdgePublisherBridge(self.adapter)
        self.state_machine = bundle["TwinStateMachine"](self.publisher)
        self.heartbeat = LinkSupervisor(
            self.config.heartbeat_timeout_ticks,
            self.config.prolonged_disconnect_ticks,
        )
        self.command_log: list[EdgeRecord] = []

    @property
    def state(self) -> str:
        return self.context.state.value

    def snapshot(self) -> EdgeRuntimeSnapshot:
        previous_state = self.context.previous_state.value if self.context.previous_state else None
        return EdgeRuntimeSnapshot(
            state=self.context.state.value,
            previous_state=previous_state,
            link_ok=self.context.link_ok,
            traction_enabled=self.context.traction_enabled,
            obstacle_active=self.context.obstacle_active,
            estop_active=self.context.estop_active,
            last_reason=self.context.last_reason,
        )

    def handle_command(self, command: EdgeCommand) -> bool:
        if command.command_type in {
            EdgeCommandType.REQUEST_MODE_MANUAL,
            EdgeCommandType.REQUEST_MODE_AUTO_LINE,
            EdgeCommandType.MANUAL_DRIVE,
            EdgeCommandType.CLEAR_SAFE_STOP,
            EdgeCommandType.ESTOP_RESET,
        }:
            self.heartbeat.observe_link_activity()

        local_rejection_reason = self._validate_locally(command)
        if local_rejection_reason is not None:
            return self._reject_locally(command, local_rejection_reason)

        twin_event = self._map_command_to_twin_event(command)
        previous_state = self.context.state.value
        accepted = self.state_machine.apply(self.context, twin_event)
        current_state = self.context.state.value
        record = EdgeRecord(
            kind="command_result",
            state=current_state,
            accepted=accepted,
            summary=command.command_type.value,
            payload={
                "previous_state": previous_state,
                "current_state": current_state,
                "corr_id": command.corr_id,
            },
            source="edge",
            corr_id=command.corr_id,
        )
        self.command_log.append(record)
        self.adapter.publish(record)
        print(
            f"[edge-transition] command={command.command_type.value} "
            f"previous={previous_state} current={current_state} accepted={accepted}"
        )
        return accepted

    def heartbeat_tick(self) -> bool:
        heartbeat_state = self.heartbeat.advance()
        if heartbeat_state == "ok":
            record = EdgeRecord(
                kind="heartbeat_tick",
                state=self.context.state.value,
                accepted=None,
                summary="heartbeat_ok",
                payload={"timeout_ticks": self.config.heartbeat_timeout_ticks},
                source="edge",
            )
            self.adapter.publish(record)
            return False
        if heartbeat_state == "degraded_wait":
            record = EdgeRecord(
                kind="heartbeat",
                state=self.context.state.value,
                accepted=None,
                summary="link_still_down",
                payload={"link_ok": False, "reason": "waiting_link_restore"},
                source="edge",
            )
            self.adapter.publish(record)
            return False

        if heartbeat_state == "heartbeat_lost":
            twin_event = self._TwinEvent(
                self._TwinEventType.HEARTBEAT_LOST,
                source="edge_system",
            )
            summary = "heartbeat_lost"
        else:
            twin_event = self._TwinEvent(
                self._TwinEventType.PROLONGED_DISCONNECT,
                source="edge_system",
            )
            summary = "prolonged_disconnect"
        previous_state = self.context.state.value
        accepted = self.state_machine.apply(self.context, twin_event)
        current_state = self.context.state.value
        record = EdgeRecord(
            kind="heartbeat_timeout" if heartbeat_state == "heartbeat_lost" else "disconnect_escalation",
            state=current_state,
            accepted=accepted,
            summary=summary,
            payload={"previous_state": previous_state, "current_state": current_state},
            source="edge",
        )
        self.command_log.append(record)
        self.adapter.publish(record)
        print(
            f"[edge-heartbeat] timeout previous={previous_state} "
            f"current={current_state} accepted={accepted}"
        )
        return accepted

    def restore_link_if_safe(self) -> bool:
        self.heartbeat.restore()
        twin_event = self._TwinEvent(
            self._TwinEventType.LINK_RESTORED_AND_SAFE,
            source="edge_system",
        )
        return self.state_machine.apply(self.context, twin_event)

    def _validate_locally(self, command: EdgeCommand) -> str | None:
        if command.command_type == EdgeCommandType.MANUAL_DRIVE:
            if self.context.state.value != "MANUAL":
                return "manual_drive_outside_manual_mode"
            if self.context.obstacle_active or self.context.estop_active or not self.context.link_ok:
                return "manual_drive_blocked_by_local_safety"
        if command.command_type == EdgeCommandType.REQUEST_MODE_AUTO_LINE and not self.context.link_ok:
            return "auto_line_request_blocked_by_link_state"
        return None

    def _reject_locally(self, command: EdgeCommand, reason: str) -> bool:
        record = EdgeRecord(
            kind="local_reject",
            state=self.context.state.value,
            accepted=False,
            summary=command.command_type.value,
            payload={"reason": reason, "command": command.command_type.value},
            source="edge",
            corr_id=command.corr_id,
        )
        self.command_log.append(record)
        self.adapter.publish(record)
        print(f"[edge-reject] command={command.command_type.value} reason={reason}")
        return False

    def _map_command_to_twin_event(self, command: EdgeCommand) -> Any:
        mapping = {
            EdgeCommandType.STARTUP_OK: self._TwinEventType.STARTUP_OK,
            EdgeCommandType.REQUEST_MODE_MANUAL: self._TwinEventType.MODE_MANUAL_REQUESTED,
            EdgeCommandType.REQUEST_MODE_AUTO_LINE: self._TwinEventType.MODE_AUTO_LINE_REQUESTED,
            EdgeCommandType.MANUAL_DRIVE: self._TwinEventType.MANUAL_COMMAND,
            EdgeCommandType.CLEAR_SAFE_STOP: self._TwinEventType.SAFE_STOP_CLEARED,
            EdgeCommandType.ESTOP_TRIGGER: self._TwinEventType.ESTOP_TRIGGERED,
            EdgeCommandType.ESTOP_RESET: self._TwinEventType.ESTOP_RESET_ACCEPTED,
            EdgeCommandType.LINK_RESTORED: self._TwinEventType.LINK_RESTORED_AND_SAFE,
            EdgeCommandType.INVALID: self._TwinEventType.INVALID_COMMAND,
        }
        return self._TwinEvent(
            mapping[command.command_type],
            source=command.source,
            payload=dict(command.payload),
            corr_id=command.corr_id,
        )
