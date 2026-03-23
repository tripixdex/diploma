from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


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

    @field_validator("requested_mode")
    @classmethod
    def validate_requested_mode(cls, value: str) -> str:
        if value not in {"MANUAL", "AUTO_LINE"}:
            raise ValueError("Разрешены только mode-команды MANUAL и AUTO_LINE.")
        return value


class ManualCommandRequest(BaseModel):
    linear: float = Field(ge=-0.3, le=0.3)
    angular: float = Field(ge=-1.0, le=1.0)
    duration_ms: int = Field(default=500, ge=100, le=5000)
    corr_id: str | None = None

    @field_validator("linear", "angular")
    @classmethod
    def reject_nan(cls, value: float) -> float:
        if value != value:
            raise ValueError("Числовые поля manual-команды не могут быть NaN.")
        return value


class ResetCommandRequest(BaseModel):
    reset_action: str = Field(min_length=1)
    state: str = Field(min_length=1)
    corr_id: str | None = None

    @field_validator("reset_action")
    @classmethod
    def validate_reset_action(cls, value: str) -> str:
        if value not in {"clear_safe_stop", "estop_reset"}:
            raise ValueError("Разрешены только reset-действия clear_safe_stop и estop_reset.")
        return value

    @field_validator("state")
    @classmethod
    def validate_state(cls, value: str) -> str:
        if value not in {"SAFE_STOP", "ESTOP_LATCHED"}:
            raise ValueError("Reset допустим только для состояний SAFE_STOP и ESTOP_LATCHED.")
        return value

    @model_validator(mode="after")
    def validate_reset_pair(self) -> "ResetCommandRequest":
        expected_state = "SAFE_STOP" if self.reset_action == "clear_safe_stop" else "ESTOP_LATCHED"
        if self.state != expected_state:
            raise ValueError(
                f"Действие {self.reset_action} разрешено только из состояния {expected_state}."
            )
        return self
