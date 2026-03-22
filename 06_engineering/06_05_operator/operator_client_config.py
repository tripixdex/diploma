from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _load_module(module_name: str, module_path: Path) -> Any:
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module {module_name} from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_TRANSPORT_DIR = Path(__file__).resolve().parents[1] / "06_03_transport"
_BACKEND_DIR = Path(__file__).resolve().parents[1] / "06_04_backend"
_TRANSPORT_CLIENT_CONFIG = _load_module(
    "mqtt_client_config",
    _TRANSPORT_DIR / "mqtt_client_config.py",
)
_TRANSPORT_CODEC = _load_module(
    "mqtt_message_codec",
    _TRANSPORT_DIR / "mqtt_message_codec.py",
)
_BACKEND_CONFIG = _load_module(
    "stage6_backend_config",
    _BACKEND_DIR / "backend_config.py",
)

SIM_CONSTANTS = _TRANSPORT_CLIENT_CONFIG.SIM_CONSTANTS
BROKER_CONFIG = _TRANSPORT_CLIENT_CONFIG.BROKER_CONFIG
CLIENT_CONFIG = _TRANSPORT_CLIENT_CONFIG.CLIENT_CONFIG
COMMAND_TOPIC_POLICIES = _TRANSPORT_CLIENT_CONFIG.COMMAND_TOPIC_POLICIES
MqttMessageCodec = _TRANSPORT_CODEC.MqttMessageCodec
DEFAULT_BACKEND_RUNTIME_CONFIG = _BACKEND_CONFIG.DEFAULT_BACKEND_RUNTIME_CONFIG


@dataclass(frozen=True, slots=True)
class OperatorApiPaths:
    health: str = "/health"
    current_status: str = "/api/status/current"
    recent_events: str = "/api/events/recent"
    recent_commands: str = "/api/commands/recent"
    recent_telemetry: str = "/api/telemetry/recent"
    live_ws: str = "/ws/live"


@dataclass(frozen=True, slots=True)
class OperatorClientConfig:
    operator_client_id: str = "agv-denford-operator-console"
    websocket_frame_limit: int = 14
    restful_limit: int = 10
    api_paths: OperatorApiPaths = OperatorApiPaths()


DEFAULT_OPERATOR_CLIENT_CONFIG = OperatorClientConfig()
