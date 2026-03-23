from __future__ import annotations

import threading
from typing import Any

import paho.mqtt.client as mqtt

from backend_config import BROKER_CONFIG, COMMAND_TOPIC_POLICIES, MqttMessageCodec, OBSERVED_TOPIC_POLICIES
from backend_storage import BackendStorageProtocol
from backend_ws import LiveStreamHub


class BackendMqttBridge:
    def __init__(
        self,
        *,
        storage: BackendStorageProtocol,
        live_hub: LiveStreamHub,
        codec: MqttMessageCodec | None = None,
        client_id: str = "agv-denford-backend",
    ) -> None:
        self.storage = storage
        self.live_hub = live_hub
        self.codec = codec or MqttMessageCodec()
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.client.on_subscribe = self._on_subscribe
        self.connected = threading.Event()
        self.subscribed = threading.Event()
        self.is_connected = False
        self._started = False

    def start(self) -> None:
        if self._started:
            return
        self.connected.clear()
        self.subscribed.clear()
        rc = self.client.connect(BROKER_CONFIG.host, BROKER_CONFIG.port, BROKER_CONFIG.keepalive)
        print(f"[backend-connect-call] rc={rc}")
        self.client.loop_start()
        if not self.connected.wait(timeout=8):
            raise RuntimeError("Backend MQTT bridge failed to connect")
        if not self.subscribed.wait(timeout=8):
            raise RuntimeError("Backend MQTT bridge failed to subscribe")
        self._started = True

    def stop(self) -> None:
        if not self._started:
            return
        self.client.loop_stop()
        self.client.disconnect()
        self.connected.clear()
        self.subscribed.clear()
        self.is_connected = False
        self._started = False

    def _on_connect(self, client: mqtt.Client, _userdata: Any, _flags: Any, reason_code: Any, _properties: Any) -> None:
        print(f"[backend-connect] reason={reason_code}")
        topics = [(policy.topic, policy.qos) for policy in (*COMMAND_TOPIC_POLICIES, *OBSERVED_TOPIC_POLICIES)]
        client.subscribe(topics)
        self.connected.set()
        self.is_connected = True

    def _on_subscribe(
        self,
        _client: mqtt.Client,
        _userdata: Any,
        _mid: int,
        reason_code_list: Any,
        _properties: Any,
    ) -> None:
        print(f"[backend-subscribe] reason_codes={reason_code_list}")
        self.subscribed.set()

    def _on_disconnect(self, _client: mqtt.Client, _userdata: Any, _flags: Any, reason_code: Any, _properties: Any) -> None:
        print(f"[backend-disconnect] reason={reason_code}")
        self.is_connected = False

    def _on_message(self, _client: mqtt.Client, _userdata: Any, message: mqtt.MQTTMessage) -> None:
        payload = self.codec.decode_payload(message.payload)
        record = self.storage.ingest_record(message.topic, payload)
        self.live_hub.publish(record.to_dict())
        print(f"[backend-ingest] topic={message.topic} category={record.category} msg_id={record.msg_id}")
