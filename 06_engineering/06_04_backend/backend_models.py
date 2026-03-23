from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(slots=True)
class BackendRecord:
    topic: str
    msg_id: str
    ts: str
    source: str
    type: str
    mode: str
    state: str
    severity: str
    payload: dict[str, Any]
    corr_id: str | None
    ack_required: bool
    received_at: str = field(default_factory=utc_now_iso)
    category: str = "event"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class BackendHealth:
    status: str
    storage_mode: str
    mqtt_bridge_connected: bool
    command_bridge_connected: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ModeCommandRequest(BaseModel):
    requested_mode: str = Field(min_length=1)
    corr_id: str | None = None


class ManualCommandRequest(BaseModel):
    linear: float
    angular: float
    duration_ms: int = Field(default=500, ge=100, le=5000)
    corr_id: str | None = None


class ResetCommandRequest(BaseModel):
    reset_action: str = Field(min_length=1)
    state: str = Field(min_length=1)
    corr_id: str | None = None
