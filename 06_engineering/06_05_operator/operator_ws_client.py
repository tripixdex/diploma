from __future__ import annotations

from collections.abc import Callable
from typing import Any

from operator_client_config import DEFAULT_OPERATOR_CLIENT_CONFIG


class OperatorWsClient:
    def __init__(self, websocket_client: Any) -> None:
        self.websocket_client = websocket_client
        self.path = DEFAULT_OPERATOR_CLIENT_CONFIG.api_paths.live_ws

    def capture_frames(
        self,
        *,
        frame_limit: int | None = None,
        on_connected: Callable[[], None] | None = None,
    ) -> list[dict[str, Any]]:
        resolved_limit = frame_limit or DEFAULT_OPERATOR_CLIENT_CONFIG.websocket_frame_limit
        frames: list[dict[str, Any]] = []
        with self.websocket_client.websocket_connect(self.path) as websocket:
            frames.append(websocket.receive_json())
            if on_connected is not None:
                on_connected()
            for _ in range(resolved_limit):
                frames.append(websocket.receive_json())
        return frames
