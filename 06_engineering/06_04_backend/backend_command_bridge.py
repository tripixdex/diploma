from __future__ import annotations

import threading
from typing import Any

import paho.mqtt.client as mqtt

from backend_config import BROKER_CONFIG, MqttMessageCodec, SIM_CONSTANTS


class BackendCommandBridge:
    def __init__(
        self,
        codec: MqttMessageCodec | None = None,
        *,
        client_id: str = "agv-denford-backend-command-bridge",
    ) -> None:
        self.codec = codec or MqttMessageCodec()
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.connected = threading.Event()
        self.is_connected = False
        self._started = False

    def start(self) -> None:
        if self._started:
            return
        self.connected.clear()
        rc = self.client.connect(BROKER_CONFIG.host, BROKER_CONFIG.port, BROKER_CONFIG.keepalive)
        print(f"[backend-command-connect-call] rc={rc}")
        self.client.loop_start()
        if not self.connected.wait(timeout=8):
            raise RuntimeError("Backend command bridge failed to connect")
        self._started = True

    def stop(self) -> None:
        if not self._started:
            return
        self.client.loop_stop()
        self.client.disconnect()
        self.connected.clear()
        self.is_connected = False
        self._started = False

    def send_mode_command(self, *, requested_mode: str, corr_id: str | None = None) -> dict[str, Any]:
        payload = self.codec.encode_mode_command(requested_mode=requested_mode, corr_id=corr_id)
        return self._publish(SIM_CONSTANTS.TOPIC_CMD_MODE, payload, qos=1, retain=False)

    def send_manual_command(
        self,
        *,
        linear: float,
        angular: float,
        duration_ms: int = 500,
        corr_id: str | None = None,
    ) -> dict[str, Any]:
        payload = self.codec.encode_manual_command(
            linear=linear,
            angular=angular,
            duration_ms=duration_ms,
            corr_id=corr_id,
        )
        return self._publish(SIM_CONSTANTS.TOPIC_CMD_MANUAL, payload, qos=1, retain=False)

    def send_reset_command(
        self,
        *,
        reset_action: str,
        state: str,
        corr_id: str | None = None,
    ) -> dict[str, Any]:
        payload = self.codec.encode_reset_command(
            reset_action=reset_action,
            state=state,
            corr_id=corr_id,
        )
        return self._publish(SIM_CONSTANTS.TOPIC_CMD_RESET, payload, qos=1, retain=False)

    def _publish(self, topic: str, payload: str, *, qos: int, retain: bool) -> dict[str, Any]:
        if not self._started:
            self.start()
        result = self.client.publish(topic, payload, qos=qos, retain=retain)
        decoded_payload = self.codec.decode_payload(payload.encode("utf-8"))
        print(f"[backend-command-publish] topic={topic} qos={qos} retain={retain} rc={result.rc}")
        return {
            "published": result.rc == mqtt.MQTT_ERR_SUCCESS,
            "topic": topic,
            "payload": payload,
            "msg_id": decoded_payload.get("msg_id"),
            "corr_id": decoded_payload.get("corr_id"),
            "ack_required": decoded_payload.get("ack_required"),
            "qos": qos,
            "retain": retain,
        }

    def _on_connect(self, _client: mqtt.Client, _userdata: Any, _flags: Any, reason_code: Any, _properties: Any) -> None:
        print(f"[backend-command-connect] reason={reason_code}")
        self.connected.set()
        self.is_connected = True

    def _on_disconnect(
        self,
        _client: mqtt.Client,
        _userdata: Any,
        _flags: Any,
        reason_code: Any,
        _properties: Any,
    ) -> None:
        print(f"[backend-command-disconnect] reason={reason_code}")
        self.is_connected = False
