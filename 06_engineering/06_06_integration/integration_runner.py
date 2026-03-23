from __future__ import annotations

import asyncio
import importlib.util
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from amqtt.broker import Broker
from fastapi.testclient import TestClient


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


def _load_backend_bundle() -> dict[str, Any]:
    backend_dir = Path(__file__).resolve().parents[1] / "06_04_backend"
    for name in [
        "backend_models",
        "backend_config",
        "backend_storage",
        "backend_ws",
        "backend_command_bridge",
        "backend_mqtt_bridge",
        "backend_api",
    ]:
        _load_module(name, backend_dir / f"{name}.py")
    backend_app = _load_module("backend_app", backend_dir / "backend_app.py")
    return {
        "build_backend_context": backend_app.build_backend_context,
        "create_backend_app": backend_app.create_backend_app,
    }


def _load_transport_bundle() -> dict[str, Any]:
    transport_dir = Path(__file__).resolve().parents[1] / "06_03_transport"
    _load_module("mqtt_client_config", transport_dir / "mqtt_client_config.py")
    codec_module = _load_module("mqtt_message_codec", transport_dir / "mqtt_message_codec.py")
    runner_module = _load_module("mqtt_transport_runner", transport_dir / "mqtt_transport_runner.py")
    return {
        "MqttMessageCodec": codec_module.MqttMessageCodec,
        "SIM_CONSTANTS": sys.modules["mqtt_client_config"].SIM_CONSTANTS,
        "BROKER_CONFIG": sys.modules["mqtt_client_config"].BROKER_CONFIG,
        "EdgeTransportGateway": runner_module.EdgeTransportGateway,
    }


def _load_operator_bundle() -> dict[str, Any]:
    operator_dir = Path(__file__).resolve().parents[1] / "06_05_operator"
    for name in [
        "operator_models",
        "operator_client_config",
        "operator_api_client",
        "operator_ws_client",
        "operator_commands",
    ]:
        _load_module(name, operator_dir / f"{name}.py")
    return {
        "BackendApiClient": sys.modules["operator_api_client"].BackendApiClient,
        "OperatorWsClient": sys.modules["operator_ws_client"].OperatorWsClient,
        "OperatorCommandPublisher": sys.modules["operator_commands"].OperatorCommandPublisher,
    }


@dataclass(slots=True)
class ScenarioResult:
    name: str
    passed: bool
    details: str


class EmbeddedBroker:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._broker: Broker | None = None
        self._ready = threading.Event()
        self._startup_error: Exception | None = None

    def start(self) -> None:
        def _run() -> None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._loop = loop
            config = {
                "listeners": {
                    "default": {"type": "tcp", "bind": f"{self.host}:{self.port}"}
                },
                "plugins": {
                    "amqtt.plugins.authentication.AnonymousAuthPlugin": {"allow_anonymous": True},
                    "amqtt.plugins.sys.broker.BrokerSysPlugin": {"sys_interval": 0},
                },
            }
            self._broker = Broker(config, loop=loop)
            try:
                loop.run_until_complete(self._broker.start())
                self._ready.set()
                loop.run_forever()
            except Exception as exc:
                self._startup_error = exc
                self._ready.set()
            finally:
                if self._broker is not None:
                    loop.run_until_complete(self._broker.shutdown())
                loop.close()

        self._thread = threading.Thread(target=_run, daemon=True)
        self._thread.start()
        self._ready.wait(timeout=5)
        if self._startup_error is not None:
            raise self._startup_error

    def stop(self) -> None:
        if self._loop is None or self._thread is None:
            return
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join(timeout=5)


def _wait_for(predicate, *, timeout: float = 8.0, step: float = 0.1) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return True
        time.sleep(step)
    return False


def _find_record(records: list[dict[str, Any]], *, category: str | None = None, field: str | None = None, value: Any = None) -> dict[str, Any] | None:
    for record in reversed(records):
        if category is not None and record.get("category") != category:
            continue
        if field is not None and record.get(field) != value:
            continue
        return record
    return None


def main() -> None:
    transport = _load_transport_bundle()
    backend = _load_backend_bundle()
    operator = _load_operator_bundle()

    codec = transport["MqttMessageCodec"]()
    sim_constants = transport["SIM_CONSTANTS"]
    broker_config = transport["BROKER_CONFIG"]
    broker = EmbeddedBroker(broker_config.host, broker_config.port)
    broker.start()
    print(f"[integration] broker_started host={broker_config.host} port={broker_config.port}")

    backend_context = backend["build_backend_context"]()
    app = backend["create_backend_app"](backend_context)
    api_test_client = TestClient(app)
    api_client = operator["BackendApiClient"](api_test_client)
    ws_client = operator["OperatorWsClient"](api_test_client)
    command_publisher = operator["OperatorCommandPublisher"](codec)
    edge_gateway = transport["EdgeTransportGateway"](codec)

    scenario_results: list[ScenarioResult] = []
    live_frames: list[dict[str, Any]] = []

    try:
        edge_gateway.start()
        backend_context.mqtt_bridge.start()
        time.sleep(1.0)
        initial_status = api_client.get_current_status()
        initial_events = api_client.get_recent_events()
        initial_telemetry = api_client.get_recent_telemetry()
        scenario_results.append(
            ScenarioResult(
                "startup full chain",
                initial_status is not None and initial_status.get("state") == "IDLE",
                f"initial_state={None if initial_status is None else initial_status.get('state')}",
            )
        )
        scenario_results.append(
            ScenarioResult(
                "operator gets initial status",
                initial_status is not None and initial_status.get("state") == "IDLE",
                f"status={initial_status}",
            )
        )

        command_publisher.start()

        def _drive_flow() -> None:
            command_publisher.send_mode_command("MANUAL", corr_id="integration-mode-001")
            command_publisher.send_manual_command(0.15, 0.0, corr_id="integration-manual-001")
            command_publisher.send_mode_command("UNSUPPORTED_MODE", corr_id="integration-mode-002")
            command_publisher.send_reset_command("clear_safe_stop", state="MANUAL", corr_id="integration-reset-001")
            for _ in range(3):
                edge_gateway.heartbeat_tick()
                time.sleep(0.5)

        live_frames = ws_client.capture_frames(frame_limit=18, on_connected=_drive_flow)

        recent_commands = api_client.get_recent_commands(limit=20)
        recent_events = api_client.get_recent_events(limit=30)
        recent_telemetry = api_client.get_recent_telemetry(limit=20)
        final_status = api_client.get_current_status()

        mode_cmd = _find_record(recent_commands, category="command", field="corr_id", value="integration-mode-001")
        manual_cmd = _find_record(recent_commands, category="command", field="corr_id", value="integration-manual-001")
        invalid_cmd = _find_record(recent_commands, category="command", field="corr_id", value="integration-mode-002")
        reset_cmd = _find_record(recent_commands, category="command", field="corr_id", value="integration-reset-001")
        accepted_mode_audit = _find_record(recent_events, field="corr_id", value=mode_cmd["msg_id"] if mode_cmd else None)
        manual_telemetry = _find_record(recent_telemetry, field="corr_id", value=manual_cmd["msg_id"] if manual_cmd else None)
        invalid_reject_audit = None
        reset_behavior_audit = None
        degraded_alarm = None
        degraded_heartbeat = None
        for record in reversed(recent_events):
            payload = record.get("payload", {})
            if record.get("topic") == sim_constants.TOPIC_EVENT_AUDIT and payload.get("result") == "rejected":
                if payload.get("reason") == "unsupported_mode_request":
                    invalid_reject_audit = record
                if payload.get("reason") == "illegal_transition" and record.get("corr_id") == (reset_cmd["msg_id"] if reset_cmd else None):
                    reset_behavior_audit = record
            if record.get("topic") == sim_constants.TOPIC_EVENT_ALARM and payload.get("reason") == "link_degraded":
                degraded_alarm = record
            if record.get("topic") == sim_constants.TOPIC_HEALTH_HEARTBEAT and payload.get("link_ok") is False:
                degraded_heartbeat = record

        scenario_results.extend(
            [
                ScenarioResult(
                    "operator sends mode command",
                    mode_cmd is not None and accepted_mode_audit is not None,
                    f"mode_cmd_found={mode_cmd is not None} accepted_audit_found={accepted_mode_audit is not None}",
                ),
                ScenarioResult(
                    "operator sends manual command",
                    manual_cmd is not None and manual_telemetry is not None,
                    f"manual_cmd_found={manual_cmd is not None} telemetry_found={manual_telemetry is not None}",
                ),
                ScenarioResult(
                    "edge emits status/telemetry/event",
                    accepted_mode_audit is not None and manual_telemetry is not None and degraded_alarm is not None,
                    f"audit={accepted_mode_audit is not None} telemetry={manual_telemetry is not None} degraded_alarm={degraded_alarm is not None}",
                ),
                ScenarioResult(
                    "backend stores and serves data",
                    final_status is not None and len(recent_commands) >= 4 and len(recent_events) >= 5 and len(recent_telemetry) >= 1,
                    f"final_status={None if final_status is None else final_status.get('state')} commands={len(recent_commands)} events={len(recent_events)} telemetry={len(recent_telemetry)}",
                ),
                ScenarioResult(
                    "operator receives live update",
                    len(live_frames) >= 10 and any(frame.get("category") == "event" for frame in live_frames if isinstance(frame, dict)),
                    f"live_frames={len(live_frames)}",
                ),
                ScenarioResult(
                    "heartbeat timeout -> degraded path",
                    final_status is not None and final_status.get("state") == "DISCONNECTED_DEGRADED" and degraded_alarm is not None and degraded_heartbeat is not None,
                    f"final_state={None if final_status is None else final_status.get('state')} degraded_alarm={degraded_alarm is not None} degraded_heartbeat={degraded_heartbeat is not None}",
                ),
                ScenarioResult(
                    "invalid command rejection",
                    invalid_cmd is not None and invalid_reject_audit is not None and final_status is not None,
                    f"invalid_cmd_found={invalid_cmd is not None} invalid_audit_found={invalid_reject_audit is not None}",
                ),
                ScenarioResult(
                    "reset/clear path behavior according to current contract",
                    reset_cmd is not None and reset_behavior_audit is not None,
                    f"reset_cmd_found={reset_cmd is not None} reset_rejection_found={reset_behavior_audit is not None}",
                ),
            ]
        )

        print("integration_summary")
        for result in scenario_results:
            status = "PASS" if result.passed else "FAIL"
            print(f"[{status}] {result.name}")
            print(f"  details: {result.details}")
        passed = sum(1 for result in scenario_results if result.passed)
        total = len(scenario_results)
        print(f"summary: passed={passed} total={total}")
        if passed != total:
            raise SystemExit(1)
    finally:
        command_publisher.stop()
        backend_context.mqtt_bridge.stop()
        edge_gateway.stop()
        broker.stop()


if __name__ == "__main__":
    main()
