from __future__ import annotations

from typing import Any

from operator_client_config import DEFAULT_OPERATOR_CLIENT_CONFIG
from operator_models import OperatorSnapshot


class BackendApiClient:
    def __init__(self, http_client: Any) -> None:
        self.http_client = http_client
        self.paths = DEFAULT_OPERATOR_CLIENT_CONFIG.api_paths

    def get_health(self) -> dict[str, Any]:
        return self.http_client.get(self.paths.health).json()

    def get_current_status(self) -> dict[str, Any] | None:
        return self.http_client.get(self.paths.current_status).json().get("status")

    def get_recent_events(self, limit: int | None = None) -> list[dict[str, Any]]:
        resolved_limit = limit or DEFAULT_OPERATOR_CLIENT_CONFIG.restful_limit
        return self.http_client.get(self.paths.recent_events, params={"limit": resolved_limit}).json().get("events", [])

    def get_recent_commands(self, limit: int | None = None) -> list[dict[str, Any]]:
        resolved_limit = limit or DEFAULT_OPERATOR_CLIENT_CONFIG.restful_limit
        return self.http_client.get(self.paths.recent_commands, params={"limit": resolved_limit}).json().get("commands", [])

    def get_recent_telemetry(self, limit: int | None = None) -> list[dict[str, Any]]:
        resolved_limit = limit or DEFAULT_OPERATOR_CLIENT_CONFIG.restful_limit
        return self.http_client.get(self.paths.recent_telemetry, params={"limit": resolved_limit}).json().get("telemetry", [])

    def build_snapshot(self) -> OperatorSnapshot:
        return OperatorSnapshot(
            current_status=self.get_current_status(),
            recent_events=self.get_recent_events(),
            recent_telemetry=self.get_recent_telemetry(),
            recent_commands=self.get_recent_commands(),
        )
