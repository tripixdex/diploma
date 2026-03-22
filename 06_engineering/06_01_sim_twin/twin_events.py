from twin_models import TwinEvent, TwinEventType


def startup_ok() -> TwinEvent:
    return TwinEvent(TwinEventType.STARTUP_OK, source="system")


def request_manual_mode() -> TwinEvent:
    return TwinEvent(TwinEventType.MODE_MANUAL_REQUESTED, source="operator")


def request_auto_line_mode() -> TwinEvent:
    return TwinEvent(TwinEventType.MODE_AUTO_LINE_REQUESTED, source="operator")


def request_safe_stop() -> TwinEvent:
    return TwinEvent(TwinEventType.SAFE_STOP_REQUESTED, source="operator")


def clear_safe_stop() -> TwinEvent:
    return TwinEvent(TwinEventType.SAFE_STOP_CLEARED, source="operator")


def obstacle_detected() -> TwinEvent:
    return TwinEvent(TwinEventType.OBSTACLE_DETECTED, source="sensor")


def estop_triggered() -> TwinEvent:
    return TwinEvent(TwinEventType.ESTOP_TRIGGERED, source="sensor")


def estop_reset() -> TwinEvent:
    return TwinEvent(TwinEventType.ESTOP_RESET_ACCEPTED, source="operator")


def heartbeat_lost() -> TwinEvent:
    return TwinEvent(TwinEventType.HEARTBEAT_LOST, source="system")


def link_restored() -> TwinEvent:
    return TwinEvent(TwinEventType.LINK_RESTORED_AND_SAFE, source="system")


def auto_line_complete() -> TwinEvent:
    return TwinEvent(TwinEventType.AUTO_LINE_COMPLETE, source="sensor")


def manual_command(linear: float, angular: float) -> TwinEvent:
    return TwinEvent(
        TwinEventType.MANUAL_COMMAND,
        source="operator",
        payload={"linear": linear, "angular": angular},
    )


def invalid_command(reason: str) -> TwinEvent:
    return TwinEvent(
        TwinEventType.INVALID_COMMAND,
        source="operator",
        payload={"reason": reason},
    )
