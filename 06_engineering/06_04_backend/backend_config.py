from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path


def _load_runtime_bootstrap():
    module_name = "agv_runtime_bootstrap"
    module_path = Path(__file__).resolve().parents[1] / "runtime_bootstrap.py"
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load runtime bootstrap from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


load_module = _load_runtime_bootstrap().load_module
_load_module = load_module


_TRANSPORT_DIR = Path(__file__).resolve().parents[1] / "06_03_transport"
_TRANSPORT_CLIENT_CONFIG = _load_module("mqtt_client_config", _TRANSPORT_DIR / "mqtt_client_config.py")
_TRANSPORT_CODEC = _load_module("mqtt_message_codec", _TRANSPORT_DIR / "mqtt_message_codec.py")

SIM_CONSTANTS = _TRANSPORT_CLIENT_CONFIG.SIM_CONSTANTS
OBSERVED_TOPIC_POLICIES = _TRANSPORT_CLIENT_CONFIG.OBSERVED_TOPIC_POLICIES
COMMAND_TOPIC_POLICIES = _TRANSPORT_CLIENT_CONFIG.COMMAND_TOPIC_POLICIES
BROKER_CONFIG = _TRANSPORT_CLIENT_CONFIG.BROKER_CONFIG
MqttMessageCodec = _TRANSPORT_CODEC.MqttMessageCodec


@dataclass(frozen=True, slots=True)
class BackendStorageConfig:
    mode: str = "dev-memory"
    postgres_dsn: str | None = None
    max_command_records: int = 100
    max_event_records: int = 200
    max_telemetry_records: int = 200


@dataclass(frozen=True, slots=True)
class BackendApiConfig:
    title: str = "AGV Denford Backend MVP"
    version: str = "stage5"


@dataclass(frozen=True, slots=True)
class BackendWsConfig:
    queue_size: int = 50
    websocket_path: str = "/ws/live"


@dataclass(frozen=True, slots=True)
class BackendCorsConfig:
    allow_origins: tuple[str, ...] = (
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:4173",
        "http://localhost:4173",
    )


@dataclass(frozen=True, slots=True)
class BackendRuntimeConfig:
    storage: BackendStorageConfig = BackendStorageConfig()
    api: BackendApiConfig = BackendApiConfig()
    ws: BackendWsConfig = BackendWsConfig()
    cors: BackendCorsConfig = BackendCorsConfig()


DEFAULT_BACKEND_RUNTIME_CONFIG = BackendRuntimeConfig()
