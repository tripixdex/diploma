from __future__ import annotations

from collections import deque
from typing import Protocol

from backend_config import DEFAULT_BACKEND_RUNTIME_CONFIG, SIM_CONSTANTS
from backend_models import BackendRecord


class BackendStorageProtocol(Protocol):
    def ingest_record(self, topic: str, message: dict) -> BackendRecord:
        ...

    def current_status(self) -> dict | None:
        ...

    def recent_events(self, limit: int = 20) -> list[dict]:
        ...

    def recent_commands(self, limit: int = 20) -> list[dict]:
        ...

    def recent_telemetry(self, limit: int = 20) -> list[dict]:
        ...


class InMemoryBackendStorage:
    """Dev/demo storage path. PostgreSQL-ready only by boundary, not by engine."""

    def __init__(self) -> None:
        cfg = DEFAULT_BACKEND_RUNTIME_CONFIG.storage
        self.mode = cfg.mode
        self._commands: deque[BackendRecord] = deque(maxlen=cfg.max_command_records)
        self._events: deque[BackendRecord] = deque(maxlen=cfg.max_event_records)
        self._telemetry: deque[BackendRecord] = deque(maxlen=cfg.max_telemetry_records)
        self._latest_status: BackendRecord | None = None

    def ingest_record(self, topic: str, message: dict) -> BackendRecord:
        record = BackendRecord(
            topic=topic,
            msg_id=message["msg_id"],
            ts=message["ts"],
            source=message["source"],
            type=message["type"],
            mode=message["mode"],
            state=message["state"],
            severity=message["severity"],
            payload=dict(message["payload"]),
            corr_id=message.get("corr_id"),
            ack_required=bool(message.get("ack_required", False)),
            category=self._classify(topic, message),
        )
        self._store(record)
        return record

    def current_status(self) -> dict | None:
        return None if self._latest_status is None else self._latest_status.to_dict()

    def recent_events(self, limit: int = 20) -> list[dict]:
        return [record.to_dict() for record in list(self._events)[-limit:]][::-1]

    def recent_commands(self, limit: int = 20) -> list[dict]:
        return [record.to_dict() for record in list(self._commands)[-limit:]][::-1]

    def recent_telemetry(self, limit: int = 20) -> list[dict]:
        return [record.to_dict() for record in list(self._telemetry)[-limit:]][::-1]

    def _store(self, record: BackendRecord) -> None:
        if record.category == "command":
            self._commands.append(record)
            return
        if record.category == "status":
            self._latest_status = record
            return
        if record.category == "telemetry":
            self._telemetry.append(record)
            return
        self._events.append(record)

    def _classify(self, topic: str, message: dict) -> str:
        if topic in {
            SIM_CONSTANTS.TOPIC_CMD_MANUAL,
            SIM_CONSTANTS.TOPIC_CMD_MODE,
            SIM_CONSTANTS.TOPIC_CMD_RESET,
        } or message["type"] == "command":
            return "command"
        if topic == SIM_CONSTANTS.TOPIC_STATE_STATUS or message["type"] == SIM_CONSTANTS.MESSAGE_TYPE_STATUS:
            return "status"
        if topic == SIM_CONSTANTS.TOPIC_STATE_TELEMETRY or message["type"] == SIM_CONSTANTS.MESSAGE_TYPE_TELEMETRY:
            return "telemetry"
        return "event"
