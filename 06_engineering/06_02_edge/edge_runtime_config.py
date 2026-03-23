from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EdgeRuntimeConfig:
    heartbeat_timeout_ticks: int = 3
    prolonged_disconnect_ticks: int = 2
    demo_manual_linear: float = 0.2
    demo_manual_angular: float = 0.0


DEFAULT_EDGE_RUNTIME_CONFIG = EdgeRuntimeConfig()
