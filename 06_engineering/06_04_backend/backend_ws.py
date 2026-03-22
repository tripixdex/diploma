from __future__ import annotations

import asyncio
import queue
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend_config import DEFAULT_BACKEND_RUNTIME_CONFIG


class LiveStreamHub:
    def __init__(self, queue_size: int | None = None) -> None:
        self._queue_size = queue_size or DEFAULT_BACKEND_RUNTIME_CONFIG.ws.queue_size
        self._subscribers: list[queue.Queue[dict[str, Any]]] = []

    def subscribe(self) -> queue.Queue[dict[str, Any]]:
        subscriber: queue.Queue[dict[str, Any]] = queue.Queue(maxsize=self._queue_size)
        self._subscribers.append(subscriber)
        return subscriber

    def unsubscribe(self, subscriber: queue.Queue[dict[str, Any]]) -> None:
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def publish(self, message: dict[str, Any]) -> None:
        for subscriber in list(self._subscribers):
            try:
                subscriber.put_nowait(message)
            except queue.Full:
                try:
                    subscriber.get_nowait()
                except queue.Empty:
                    pass
                subscriber.put_nowait(message)


def build_ws_router(hub: LiveStreamHub) -> APIRouter:
    router = APIRouter()
    ws_path = DEFAULT_BACKEND_RUNTIME_CONFIG.ws.websocket_path

    @router.websocket(ws_path)
    async def live_feed(websocket: WebSocket) -> None:
        await websocket.accept()
        await websocket.send_json({"type": "ws_status", "status": "connected"})
        subscriber = hub.subscribe()
        try:
            while True:
                try:
                    message = await asyncio.to_thread(subscriber.get, True, 10)
                except queue.Empty:
                    await websocket.send_json({"type": "ws_keepalive", "status": "idle"})
                    continue
                await websocket.send_json(message)
        except WebSocketDisconnect:
            pass
        finally:
            hub.unsubscribe(subscriber)

    return router
