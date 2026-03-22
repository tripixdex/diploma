from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class OperatorSnapshot:
    current_status: dict[str, Any] | None = None
    recent_events: list[dict[str, Any]] = field(default_factory=list)
    recent_telemetry: list[dict[str, Any]] = field(default_factory=list)
    recent_commands: list[dict[str, Any]] = field(default_factory=list)
    live_frames: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class OperatorCommandReceipt:
    topic: str
    payload: str
    qos: int
    retain: bool


@dataclass(slots=True)
class OperatorRunSummary:
    initial_status: dict[str, Any] | None
    final_status: dict[str, Any] | None
    event_count: int
    telemetry_count: int
    command_count: int
    live_frame_count: int
