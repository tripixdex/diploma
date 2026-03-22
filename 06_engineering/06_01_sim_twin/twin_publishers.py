from __future__ import annotations

from itertools import count

from twin_models import PublishedMessage, TwinContext, TwinEvent


class InMemoryPublisher:
    def __init__(self) -> None:
        self.messages: list[PublishedMessage] = []
        self._seq = count(1)

    def publish(self, topic: str, msg_type: str, context: TwinContext, event: TwinEvent, **payload: object) -> None:
        msg_id = f"sim-{next(self._seq):04d}"
        message = PublishedMessage(
            topic=topic,
            payload={
                "msg_id": msg_id,
                "ts": "SIM_TIME",
                "source": event.source,
                "type": msg_type,
                "mode": context.state.value,
                "state": context.state.value,
                "severity": payload.pop("severity", "info"),
                "payload": payload,
                "corr_id": event.corr_id,
                "ack_required": False,
            },
        )
        self.messages.append(message)
        print(f"[publish] {topic} {message.payload}")

    def publish_status(self, context: TwinContext, event: TwinEvent) -> None:
        self.publish(
            "agv/denford/v1/state/status",
            "status",
            context,
            event,
            prev_state=context.previous_state.value if context.previous_state else None,
            transition_reason=context.last_reason,
            traction_enabled=context.traction_enabled,
        )

    def publish_audit(self, context: TwinContext, event: TwinEvent, result: str, reason: str) -> None:
        self.publish(
            "agv/denford/v1/event/audit",
            "audit",
            context,
            event,
            severity="info" if result == "accepted" else "warning",
            result=result,
            reason=reason,
            event_type=event.event_type.value,
        )

    def publish_alarm(self, context: TwinContext, event: TwinEvent, reason: str) -> None:
        self.publish(
            "agv/denford/v1/event/alarm",
            "alarm",
            context,
            event,
            severity="warning",
            reason=reason,
        )

    def publish_fault(self, context: TwinContext, event: TwinEvent, reason: str) -> None:
        self.publish(
            "agv/denford/v1/event/fault",
            "fault",
            context,
            event,
            severity="critical",
            reason=reason,
        )

    def publish_heartbeat(self, context: TwinContext, event: TwinEvent, link_ok: bool) -> None:
        self.publish(
            "agv/denford/v1/health/heartbeat",
            "heartbeat",
            context,
            event,
            link_ok=link_ok,
        )

    def publish_telemetry(self, context: TwinContext, event: TwinEvent, **telemetry: object) -> None:
        self.publish(
            "agv/denford/v1/state/telemetry",
            "telemetry",
            context,
            event,
            **telemetry,
        )
