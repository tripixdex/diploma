from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EdgeCommandType(str, Enum):
    STARTUP_OK = "startup_ok"
    REQUEST_MODE_MANUAL = "request_mode_manual"
    REQUEST_MODE_AUTO_LINE = "request_mode_auto_line"
    MANUAL_DRIVE = "manual_drive"
    CLEAR_SAFE_STOP = "clear_safe_stop"
    ESTOP_TRIGGER = "estop_trigger"
    ESTOP_RESET = "estop_reset"
    LINK_RESTORED = "link_restored"
    INVALID = "invalid"


@dataclass(slots=True)
class EdgeCommand:
    command_type: EdgeCommandType
    source: str = "edge_operator"
    payload: dict[str, Any] = field(default_factory=dict)
    corr_id: str | None = None


@dataclass(slots=True)
class EdgeRuntimeSnapshot:
    state: str
    previous_state: str | None
    link_ok: bool
    traction_enabled: bool
    obstacle_active: bool
    estop_active: bool
    last_reason: str | None


@dataclass(slots=True)
class EdgeRecord:
    kind: str
    state: str
    accepted: bool | None
    summary: str
    payload: dict[str, Any] = field(default_factory=dict)
    source: str = "edge"
    corr_id: str | None = None
