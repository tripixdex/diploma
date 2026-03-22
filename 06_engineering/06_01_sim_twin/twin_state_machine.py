from __future__ import annotations

from twin_models import TwinContext, TwinEvent, TwinEventType, TwinState
from twin_publishers import InMemoryPublisher


class TwinStateMachine:
    def __init__(self, publisher: InMemoryPublisher) -> None:
        self.publisher = publisher
        self.allowed_transitions: dict[tuple[TwinState, TwinEventType], TwinState] = {
            (TwinState.INIT, TwinEventType.STARTUP_OK): TwinState.IDLE,
            (TwinState.INIT, TwinEventType.STARTUP_FAULT): TwinState.FAULT,
            (TwinState.IDLE, TwinEventType.MODE_MANUAL_REQUESTED): TwinState.MANUAL,
            (TwinState.IDLE, TwinEventType.MODE_AUTO_LINE_REQUESTED): TwinState.AUTO_LINE,
            (TwinState.IDLE, TwinEventType.SAFE_STOP_REQUESTED): TwinState.SAFE_STOP,
            (TwinState.IDLE, TwinEventType.ESTOP_TRIGGERED): TwinState.ESTOP_LATCHED,
            (TwinState.IDLE, TwinEventType.FAULT_DETECTED): TwinState.FAULT,
            (TwinState.MANUAL, TwinEventType.MANUAL_STOP_REQUESTED): TwinState.IDLE,
            (TwinState.MANUAL, TwinEventType.SAFE_STOP_REQUESTED): TwinState.SAFE_STOP,
            (TwinState.MANUAL, TwinEventType.OBSTACLE_DETECTED): TwinState.SAFE_STOP,
            (TwinState.MANUAL, TwinEventType.ESTOP_TRIGGERED): TwinState.ESTOP_LATCHED,
            (TwinState.MANUAL, TwinEventType.HEARTBEAT_LOST): TwinState.DISCONNECTED_DEGRADED,
            (TwinState.MANUAL, TwinEventType.FAULT_DETECTED): TwinState.FAULT,
            (TwinState.AUTO_LINE, TwinEventType.AUTO_LINE_COMPLETE): TwinState.IDLE,
            (TwinState.AUTO_LINE, TwinEventType.SAFE_STOP_REQUESTED): TwinState.SAFE_STOP,
            (TwinState.AUTO_LINE, TwinEventType.OBSTACLE_DETECTED): TwinState.SAFE_STOP,
            (TwinState.AUTO_LINE, TwinEventType.ESTOP_TRIGGERED): TwinState.ESTOP_LATCHED,
            (TwinState.AUTO_LINE, TwinEventType.HEARTBEAT_LOST): TwinState.DISCONNECTED_DEGRADED,
            (TwinState.AUTO_LINE, TwinEventType.FAULT_DETECTED): TwinState.FAULT,
            (TwinState.SAFE_STOP, TwinEventType.SAFE_STOP_CLEARED): TwinState.IDLE,
            (TwinState.SAFE_STOP, TwinEventType.ESTOP_TRIGGERED): TwinState.ESTOP_LATCHED,
            (TwinState.SAFE_STOP, TwinEventType.FAULT_DETECTED): TwinState.FAULT,
            (TwinState.ESTOP_LATCHED, TwinEventType.ESTOP_RESET_ACCEPTED): TwinState.IDLE,
            (TwinState.DISCONNECTED_DEGRADED, TwinEventType.LINK_RESTORED_AND_SAFE): TwinState.IDLE,
            (TwinState.DISCONNECTED_DEGRADED, TwinEventType.SAFE_STOP_REQUESTED): TwinState.SAFE_STOP,
            (TwinState.DISCONNECTED_DEGRADED, TwinEventType.ESTOP_TRIGGERED): TwinState.ESTOP_LATCHED,
            (TwinState.DISCONNECTED_DEGRADED, TwinEventType.FAULT_DETECTED): TwinState.FAULT,
            (TwinState.FAULT, TwinEventType.FAULT_RESET_ACCEPTED): TwinState.IDLE,
        }

    def apply(self, context: TwinContext, event: TwinEvent) -> bool:
        if event.event_type == TwinEventType.MANUAL_COMMAND:
            return self._handle_manual_command(context, event)
        if event.event_type == TwinEventType.INVALID_COMMAND:
            self.publisher.publish_audit(context, event, "rejected", event.payload.get("reason", "invalid_command"))
            return False

        target = self.allowed_transitions.get((context.state, event.event_type))
        if target is None:
            self.publisher.publish_audit(context, event, "rejected", "illegal_transition")
            return False

        self._before_transition(context, event)
        context.previous_state = context.state
        context.state = target
        context.last_reason = event.event_type.value
        self._after_transition(context, event)
        return True

    def _before_transition(self, context: TwinContext, event: TwinEvent) -> None:
        if event.event_type == TwinEventType.OBSTACLE_DETECTED:
            context.obstacle_active = True
        if event.event_type == TwinEventType.ESTOP_TRIGGERED:
            context.estop_active = True
        if event.event_type == TwinEventType.HEARTBEAT_LOST:
            context.link_ok = False

    def _after_transition(self, context: TwinContext, event: TwinEvent) -> None:
        context.traction_enabled = context.state in {TwinState.MANUAL, TwinState.AUTO_LINE}
        if event.event_type == TwinEventType.SAFE_STOP_CLEARED:
            context.obstacle_active = False
        if event.event_type == TwinEventType.ESTOP_RESET_ACCEPTED:
            context.estop_active = False
        if event.event_type == TwinEventType.LINK_RESTORED_AND_SAFE:
            context.link_ok = True

        self.publisher.publish_audit(context, event, "accepted", event.event_type.value)
        self.publisher.publish_status(context, event)

        if context.state == TwinState.SAFE_STOP:
            self.publisher.publish_alarm(context, event, context.last_reason or "safe_stop")
        if context.state == TwinState.ESTOP_LATCHED:
            self.publisher.publish_alarm(context, event, "estop_latched")
            self.publisher.publish_fault(context, event, "estop_latched")
        if context.state == TwinState.FAULT:
            self.publisher.publish_fault(context, event, context.last_reason or "fault")
        if context.state == TwinState.DISCONNECTED_DEGRADED:
            self.publisher.publish_alarm(context, event, "link_degraded")
        if context.state == TwinState.AUTO_LINE:
            self.publisher.publish_telemetry(
                context,
                event,
                line_sensor_state="line_detected",
                traction_enabled=context.traction_enabled,
            )
        if event.event_type == TwinEventType.AUTO_LINE_COMPLETE:
            self.publisher.publish_telemetry(
                context,
                event,
                docking_state="dock_complete",
                traction_enabled=context.traction_enabled,
            )

        self.publisher.publish_heartbeat(context, event, link_ok=context.link_ok)

    def _handle_manual_command(self, context: TwinContext, event: TwinEvent) -> bool:
        if context.state != TwinState.MANUAL:
            self.publisher.publish_audit(context, event, "rejected", "manual_command_outside_manual_mode")
            return False
        if context.obstacle_active or context.estop_active or not context.link_ok:
            self.publisher.publish_audit(context, event, "rejected", "manual_command_blocked_by_safety")
            return False

        context.last_reason = event.event_type.value
        self.publisher.publish_audit(context, event, "accepted", "manual_command_accepted")
        self.publisher.publish_telemetry(
            context,
            event,
            linear=event.payload.get("linear", 0.0),
            angular=event.payload.get("angular", 0.0),
            traction_enabled=context.traction_enabled,
        )
        self.publisher.publish_heartbeat(context, event, link_ok=context.link_ok)
        return True
