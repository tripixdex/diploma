from __future__ import annotations

import time

import paho.mqtt.client as mqtt

from operator_client_config import BROKER_CONFIG, DEFAULT_OPERATOR_CLIENT_CONFIG, MqttMessageCodec, SIM_CONSTANTS
from operator_models import OperatorCommandReceipt


class OperatorCommandPublisher:
    def __init__(self, codec: MqttMessageCodec | None = None) -> None:
        self.codec = codec or MqttMessageCodec()
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=DEFAULT_OPERATOR_CLIENT_CONFIG.operator_client_id,
        )
        self.client.on_connect = lambda _client, _userdata, _flags, reason_code, _properties: print(
            f"[operator-connect] reason={reason_code}"
        )
        self.client.on_disconnect = lambda _client, _userdata, _flags, reason_code, _properties: print(
            f"[operator-disconnect] reason={reason_code}"
        )

    def start(self) -> None:
        rc = self.client.connect(BROKER_CONFIG.host, BROKER_CONFIG.port, BROKER_CONFIG.keepalive)
        print(f"[operator-connect-call] rc={rc}")
        self.client.loop_start()
        time.sleep(0.5)

    def stop(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()

    def send_mode_command(self, requested_mode: str, corr_id: str) -> OperatorCommandReceipt:
        payload = self.codec.encode_mode_command(requested_mode=requested_mode, corr_id=corr_id)
        return self._publish(SIM_CONSTANTS.TOPIC_CMD_MODE, payload, qos=1, retain=False)

    def send_manual_command(self, linear: float, angular: float, corr_id: str) -> OperatorCommandReceipt:
        payload = self.codec.encode_manual_command(linear=linear, angular=angular, corr_id=corr_id)
        return self._publish(SIM_CONSTANTS.TOPIC_CMD_MANUAL, payload, qos=1, retain=False)

    def send_reset_command(self, reset_action: str, state: str, corr_id: str) -> OperatorCommandReceipt:
        payload = self.codec.encode_reset_command(reset_action=reset_action, state=state, corr_id=corr_id)
        return self._publish(SIM_CONSTANTS.TOPIC_CMD_RESET, payload, qos=1, retain=False)

    def _publish(self, topic: str, payload: str, *, qos: int, retain: bool) -> OperatorCommandReceipt:
        self.client.publish(topic, payload, qos=qos, retain=retain)
        print(f"[operator-publish] topic={topic} qos={qos} retain={retain} payload={payload}")
        time.sleep(0.8)
        return OperatorCommandReceipt(topic=topic, payload=payload, qos=qos, retain=retain)
