from __future__ import annotations

from fastapi import APIRouter

from backend_models import BackendHealth
from backend_storage import BackendStorageProtocol


def build_api_router(storage: BackendStorageProtocol, health_provider) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def health() -> dict:
        health_model = BackendHealth(**health_provider())
        return health_model.to_dict()

    @router.get("/api/status/current")
    def current_status() -> dict:
        return {"status": storage.current_status()}

    @router.get("/api/events/recent")
    def recent_events(limit: int = 20) -> dict:
        return {"events": storage.recent_events(limit)}

    @router.get("/api/commands/recent")
    def recent_commands(limit: int = 20) -> dict:
        return {"commands": storage.recent_commands(limit)}

    @router.get("/api/telemetry/recent")
    def recent_telemetry(limit: int = 20) -> dict:
        return {"telemetry": storage.recent_telemetry(limit)}

    return router
