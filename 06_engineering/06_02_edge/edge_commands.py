from __future__ import annotations

from edge_models import EdgeCommand, EdgeCommandType


def startup_ok() -> EdgeCommand:
    return EdgeCommand(EdgeCommandType.STARTUP_OK, source="edge_system")


def request_manual_mode() -> EdgeCommand:
    return EdgeCommand(EdgeCommandType.REQUEST_MODE_MANUAL)


def request_auto_line_mode() -> EdgeCommand:
    return EdgeCommand(EdgeCommandType.REQUEST_MODE_AUTO_LINE)


def manual_drive(linear: float, angular: float) -> EdgeCommand:
    return EdgeCommand(
        EdgeCommandType.MANUAL_DRIVE,
        payload={"linear": linear, "angular": angular},
    )


def clear_safe_stop() -> EdgeCommand:
    return EdgeCommand(EdgeCommandType.CLEAR_SAFE_STOP)


def estop_trigger() -> EdgeCommand:
    return EdgeCommand(EdgeCommandType.ESTOP_TRIGGER, source="edge_sensor")


def estop_reset() -> EdgeCommand:
    return EdgeCommand(EdgeCommandType.ESTOP_RESET)


def link_restored() -> EdgeCommand:
    return EdgeCommand(EdgeCommandType.LINK_RESTORED, source="edge_system")


def invalid_command(reason: str) -> EdgeCommand:
    return EdgeCommand(
        EdgeCommandType.INVALID,
        payload={"reason": reason},
    )
