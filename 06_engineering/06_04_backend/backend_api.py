from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend_command_bridge import BackendCommandBridge
from backend_models import BackendHealth, ManualCommandRequest, ModeCommandRequest, ResetCommandRequest
from backend_storage import BackendStorageProtocol


def build_api_router(
    storage: BackendStorageProtocol,
    health_provider,
    command_bridge: BackendCommandBridge,
) -> APIRouter:
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

    @router.post("/api/control/mode")
    def send_mode_command(request: ModeCommandRequest) -> dict:
        try:
            return command_bridge.send_mode_command(
                requested_mode=request.requested_mode,
                corr_id=request.corr_id,
            )
        except Exception as exc:
            raise HTTPException(status_code=503, detail=f"mode command dispatch failed: {exc}") from exc

    @router.post("/api/control/manual")
    def send_manual_command(request: ManualCommandRequest) -> dict:
        try:
            return command_bridge.send_manual_command(
                linear=request.linear,
                angular=request.angular,
                duration_ms=request.duration_ms,
                corr_id=request.corr_id,
            )
        except Exception as exc:
            raise HTTPException(status_code=503, detail=f"manual command dispatch failed: {exc}") from exc

    @router.post("/api/control/reset")
    def send_reset_command(request: ResetCommandRequest) -> dict:
        try:
            return command_bridge.send_reset_command(
                reset_action=request.reset_action,
                state=request.state,
                corr_id=request.corr_id,
            )
        except Exception as exc:
            raise HTTPException(status_code=503, detail=f"reset command dispatch failed: {exc}") from exc

    return router
