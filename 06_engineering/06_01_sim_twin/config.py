from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TwinRuntimeConfig:
    message_id_prefix: str = "sim"
    timestamp_placeholder: str = "SIM_TIME"
    ack_required_default: bool = False
    demo_manual_linear: float = 0.2
    demo_manual_angular: float = 0.0


DEFAULT_CONFIG = TwinRuntimeConfig()
