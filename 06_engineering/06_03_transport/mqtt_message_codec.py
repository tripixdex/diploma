from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any

from mqtt_client_config import SIM_CONSTANTS, TOPIC_POLICY_BY_KIND


class MqttMessageCodec:
    def _base_message(
        self,
        *,
        msg_type: str,
        source: str,
        mode: str,
        state: str,
        severity: str,
        payload: dict[str, Any],
        corr_id: str | None,
        ack_required: bool,
        msg_id_prefix: str,
    ) -> dict[str, Any]:
        return {
            "msg_id": f"{msg_id_prefix}-{uuid.uuid4().hex[:10]}",
            "ts": datetime.now(timezone.utc).isoformat(),
            "source": source,
            "type": msg_type,
            "mode": mode,
            "state": state,
            "severity": severity,
            "payload": payload,
            "corr_id": corr_id,
            "ack_required": ack_required,
        }

    def encode_event_message(
        self,
        *,
        kind: str,
        mode: str,
        state: str,
        payload: dict[str, Any],
        corr_id: str | None = None,
        source: str = "edge",
        severity: str | None = None,
    ) -> str:
        resolved_severity = severity or self._default_severity_for_kind(kind, payload)
        return json.dumps(
            self._base_message(
                msg_type=kind,
                source=source,
                mode=mode,
                state=state,
                severity=resolved_severity,
                payload=payload,
                corr_id=corr_id,
                ack_required=False,
                msg_id_prefix=kind,
            )
        )

    def encode_mode_command(
        self,
        *,
        requested_mode: str,
        state: str = "IDLE",
        corr_id: str | None = None,
        source: str = SIM_CONSTANTS.SOURCE_OPERATOR,
        reason: str = "operator_request",
    ) -> str:
        return json.dumps(
            self._base_message(
                msg_type="command",
                source=source,
                mode=requested_mode,
                state=state,
                severity=SIM_CONSTANTS.SEVERITY_INFO,
                payload={"requested_mode": requested_mode, "reason": reason},
                corr_id=corr_id,
                ack_required=True,
                msg_id_prefix="cmd-mode",
            )
        )

    def encode_manual_command(
        self,
        *,
        linear: float,
        angular: float,
        duration_ms: int = 500,
        state: str = "MANUAL",
        corr_id: str | None = None,
        source: str = SIM_CONSTANTS.SOURCE_OPERATOR,
    ) -> str:
        return json.dumps(
            self._base_message(
                msg_type="command",
                source=source,
                mode="MANUAL",
                state=state,
                severity=SIM_CONSTANTS.SEVERITY_INFO,
                payload={
                    "linear": linear,
                    "angular": angular,
                    "duration_ms": duration_ms,
                },
                corr_id=corr_id,
                ack_required=True,
                msg_id_prefix="cmd-manual",
            )
        )

    def encode_reset_command(
        self,
        *,
        reset_action: str,
        state: str,
        corr_id: str | None = None,
        source: str = SIM_CONSTANTS.SOURCE_OPERATOR,
    ) -> str:
        return json.dumps(
            self._base_message(
                msg_type="command",
                source=source,
                mode=state,
                state=state,
                severity=SIM_CONSTANTS.SEVERITY_INFO,
                payload={"reset_action": reset_action},
                corr_id=corr_id,
                ack_required=True,
                msg_id_prefix="cmd-reset",
            )
        )

    def decode_payload(self, payload_bytes: bytes) -> dict[str, Any]:
        return json.loads(payload_bytes.decode("utf-8"))

    def _default_severity_for_kind(self, kind: str, payload: dict[str, Any]) -> str:
        if kind == "audit":
            return (
                SIM_CONSTANTS.SEVERITY_INFO
                if payload.get("result") == SIM_CONSTANTS.AUDIT_RESULT_ACCEPTED
                else SIM_CONSTANTS.SEVERITY_WARNING
            )
        if kind == "alarm":
            return SIM_CONSTANTS.SEVERITY_WARNING
        if kind == "fault":
            return SIM_CONSTANTS.SEVERITY_CRITICAL
        return SIM_CONSTANTS.SEVERITY_INFO

    def topic_for_kind(self, kind: str) -> str:
        return TOPIC_POLICY_BY_KIND[kind].topic
