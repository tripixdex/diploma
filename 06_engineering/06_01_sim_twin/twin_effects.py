from __future__ import annotations

from publisher_protocol import PublisherProtocol
from twin_models import TransitionDecision, TwinContext, TwinEvent


class TwinEffectDispatcher:
    def __init__(self, publisher: PublisherProtocol) -> None:
        self.publisher = publisher

    def dispatch(self, context: TwinContext, event: TwinEvent, decision: TransitionDecision) -> None:
        self.publisher.publish_audit(context, event, decision.audit_result, decision.audit_reason)

        if decision.publish_status:
            self.publisher.publish_status(context, event)
        if decision.alarm_reason:
            self.publisher.publish_alarm(context, event, decision.alarm_reason)
        if decision.fault_reason:
            self.publisher.publish_fault(context, event, decision.fault_reason)
        if decision.telemetry_payload:
            self.publisher.publish_telemetry(context, event, **decision.telemetry_payload)
        if decision.publish_heartbeat:
            self.publisher.publish_heartbeat(context, event, link_ok=decision.heartbeat_link_ok)
