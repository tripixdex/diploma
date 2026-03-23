from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TwinState(str, Enum):
    INIT = "INIT"
    IDLE = "IDLE"
    MANUAL = "MANUAL"
    AUTO_LINE = "AUTO_LINE"
    SAFE_STOP = "SAFE_STOP"
    ESTOP_LATCHED = "ESTOP_LATCHED"
    FAULT = "FAULT"
    DISCONNECTED_DEGRADED = "DISCONNECTED_DEGRADED"
    MAINTENANCE = "MAINTENANCE"


class TwinEventType(str, Enum):
    STARTUP_OK = "startup_ok"
    STARTUP_FAULT = "startup_fault"
    MODE_MANUAL_REQUESTED = "mode_manual_requested"
    MODE_AUTO_LINE_REQUESTED = "mode_auto_line_requested"
    MODE_IDLE_REQUESTED = "mode_idle_requested"
    MANUAL_STOP_REQUESTED = "manual_stop_requested"
    SAFE_STOP_REQUESTED = "safe_stop_requested"
    SAFE_STOP_CLEARED = "safe_stop_cleared"
    OBSTACLE_DETECTED = "obstacle_detected"
    ESTOP_TRIGGERED = "estop_triggered"
    ESTOP_RESET_ACCEPTED = "estop_reset_accepted"
    FAULT_DETECTED = "fault_detected"
    FAULT_RESET_ACCEPTED = "fault_reset_accepted"
    HEARTBEAT_LOST = "heartbeat_lost"
    PROLONGED_DISCONNECT = "prolonged_disconnect"
    LINK_RESTORED_AND_SAFE = "link_restored_and_safe"
    AUTO_LINE_COMPLETE = "auto_line_complete"
    MANUAL_COMMAND = "manual_command"
    INVALID_COMMAND = "invalid_command"


@dataclass(slots=True)
class TwinEvent:
    event_type: TwinEventType
    source: str = "twin"
    payload: dict[str, Any] = field(default_factory=dict)
    corr_id: str | None = None


@dataclass(slots=True)
class PublishedMessage:
    topic: str
    payload: dict[str, Any]


@dataclass(slots=True)
class TwinContext:
    state: TwinState = TwinState.INIT
    previous_state: TwinState | None = None
    obstacle_active: bool = False
    estop_active: bool = False
    link_ok: bool = True
    traction_enabled: bool = False
    last_reason: str | None = None
