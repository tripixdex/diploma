from __future__ import annotations

from dataclasses import dataclass

from fastapi import FastAPI

from backend_api import build_api_router
from backend_config import DEFAULT_BACKEND_RUNTIME_CONFIG
from backend_mqtt_bridge import BackendMqttBridge
from backend_storage import InMemoryBackendStorage
from backend_ws import LiveStreamHub, build_ws_router


@dataclass(slots=True)
class BackendContext:
    storage: InMemoryBackendStorage
    live_hub: LiveStreamHub
    mqtt_bridge: BackendMqttBridge


def build_backend_context() -> BackendContext:
    storage = InMemoryBackendStorage()
    live_hub = LiveStreamHub()
    mqtt_bridge = BackendMqttBridge(storage=storage, live_hub=live_hub)
    return BackendContext(storage=storage, live_hub=live_hub, mqtt_bridge=mqtt_bridge)


def create_backend_app(context: BackendContext | None = None) -> FastAPI:
    resolved_context = context or build_backend_context()
    app = FastAPI(
        title=DEFAULT_BACKEND_RUNTIME_CONFIG.api.title,
        version=DEFAULT_BACKEND_RUNTIME_CONFIG.api.version,
    )

    def _health_provider() -> dict:
        return {
            "status": "ok",
            "storage_mode": resolved_context.storage.mode,
            "mqtt_bridge_connected": resolved_context.mqtt_bridge.is_connected,
        }

    app.state.backend_context = resolved_context
    app.include_router(build_api_router(resolved_context.storage, _health_provider))
    app.include_router(build_ws_router(resolved_context.live_hub))
    return app
