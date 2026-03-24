from __future__ import annotations

import importlib.util
import sys
import threading
import time
from pathlib import Path
from typing import Any

import paho.mqtt.client as mqtt

from mqtt_client_config import BROKER_CONFIG, CLIENT_CONFIG, COMMAND_TOPIC_POLICIES, OBSERVED_TOPIC_POLICIES, SIM_CONSTANTS, TOPIC_POLICY_BY_KIND
from mqtt_message_codec import MqttMessageCodec


def _load_runtime_bootstrap() -> Any:
    module_name = "agv_runtime_bootstrap"
    module_path = Path(__file__).resolve().parents[1] / "runtime_bootstrap.py"
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load runtime bootstrap from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


_RUNTIME_BOOTSTRAP = _load_runtime_bootstrap()
EmbeddedBroker = _RUNTIME_BOOTSTRAP.EmbeddedBroker
load_module = _RUNTIME_BOOTSTRAP.load_module
_load_module = load_module


def _load_edge_modules() -> dict[str, Any]:
    edge_dir = Path(__file__).resolve().parents[1] / "06_02_edge"
    for name in [
        "edge_models",
        "edge_adapter_protocol",
        "edge_heartbeat",
        "edge_runtime_config",
        "edge_commands",
    ]:
        _load_module(name, edge_dir / f"{name}.py")
    edge_runtime_module = _load_module("edge_runtime", edge_dir / "edge_runtime.py")
    edge_commands_module = sys.modules["edge_commands"]
    return {
        "EdgeRuntime": edge_runtime_module.EdgeRuntime,
        "startup_ok": edge_commands_module.startup_ok,
    }
class ConsoleObserver:
    def __init__(self, client_id: str, codec: MqttMessageCodec) -> None:
        self.codec = codec
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_connect_fail = self._on_connect_fail
        self.client.on_subscribe = self._on_subscribe
        self.client.on_message = self._on_message
        self.messages: list[tuple[str, dict[str, Any]]] = []
        self.connected = threading.Event()
        self.subscribed = threading.Event()

    def start(self) -> None:
        rc = self.client.connect(BROKER_CONFIG.host, BROKER_CONFIG.port, BROKER_CONFIG.keepalive)
        print(f"[observer-connect-call] client_id={self.client._client_id.decode()} rc={rc}")
        self.client.loop_start()
        if not self.connected.wait(timeout=8):
            raise RuntimeError("Observer failed to connect to MQTT broker")
        if not self.subscribed.wait(timeout=8):
            raise RuntimeError("Observer failed to subscribe to MQTT topics")

    def stop(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()

    def _on_connect(self, client: mqtt.Client, _userdata: Any, _flags: Any, reason_code: Any, _properties: Any) -> None:
        print(f"[observer-connect] client_id={client._client_id.decode()} reason={reason_code}")
        client.subscribe([(policy.topic, policy.qos) for policy in OBSERVED_TOPIC_POLICIES])
        self.connected.set()

    def _on_subscribe(
        self,
        client: mqtt.Client,
        _userdata: Any,
        _mid: int,
        reason_code_list: Any,
        _properties: Any,
    ) -> None:
        print(f"[observer-subscribe] client_id={client._client_id.decode()} reason_codes={reason_code_list}")
        self.subscribed.set()

    def _on_disconnect(self, client: mqtt.Client, _userdata: Any, _flags: Any, reason_code: Any, _properties: Any) -> None:
        print(f"[observer-disconnect] client_id={client._client_id.decode()} reason={reason_code}")

    def _on_connect_fail(self, client: mqtt.Client, _userdata: Any) -> None:
        print(f"[observer-connect-fail] client_id={client._client_id.decode()}")

    def _on_message(self, _client: mqtt.Client, _userdata: Any, message: mqtt.MQTTMessage) -> None:
        payload = self.codec.decode_payload(message.payload)
        self.messages.append((message.topic, payload))
        print(f"[observer-message] topic={message.topic} payload={payload}")


class MqttEdgeAdapter:
    def __init__(self, client: mqtt.Client, codec: MqttMessageCodec) -> None:
        self.client = client
        self.codec = codec

    def publish(self, record: Any) -> None:
        if record.kind in TOPIC_POLICY_BY_KIND:
            self._publish_contract_record(record)
            return
        if record.kind == "local_reject":
            self._publish_local_reject(record)
            return
        print(
            f"[edge-transport-internal] kind={record.kind} state={record.state} "
            f"accepted={record.accepted} payload={record.payload}"
        )

    def _publish_contract_record(self, record: Any) -> None:
        policy = TOPIC_POLICY_BY_KIND[record.kind]
        payload = self.codec.encode_event_message(
            kind=record.kind,
            mode=record.state,
            state=record.state,
            payload=dict(record.payload),
            corr_id=record.corr_id,
            source="edge",
        )
        self.client.publish(policy.topic, payload, qos=policy.qos, retain=policy.retain)
        print(f"[edge-mqtt-publish] topic={policy.topic} qos={policy.qos} retain={policy.retain}")

    def _publish_local_reject(self, record: Any) -> None:
        payload = self.codec.encode_event_message(
            kind="audit",
            mode=record.state,
            state=record.state,
            payload={
                "result": SIM_CONSTANTS.AUDIT_RESULT_REJECTED,
                "reason": record.payload.get("reason"),
                "requested_action": record.payload.get("command"),
                "current_state": record.state,
            },
            corr_id=record.corr_id,
            source="edge",
            severity=SIM_CONSTANTS.SEVERITY_WARNING,
        )
        policy = TOPIC_POLICY_BY_KIND["audit"]
        self.client.publish(policy.topic, payload, qos=policy.qos, retain=policy.retain)
        print(f"[edge-mqtt-publish] topic={policy.topic} qos={policy.qos} retain={policy.retain}")


class EdgeTransportGateway:
    def __init__(self, codec: MqttMessageCodec) -> None:
        modules = _load_edge_modules()
        self.codec = codec
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_CONFIG.edge_client_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        self.client.on_subscribe = self._on_subscribe
        self._connected = threading.Event()
        self._subscribed = threading.Event()
        self._bootstrapped = False
        self._lock = threading.Lock()
        self._startup_ok = modules["startup_ok"]
        self.runtime = modules["EdgeRuntime"](adapter=MqttEdgeAdapter(self.client, self.codec))

    def start(self) -> None:
        rc = self.client.connect(BROKER_CONFIG.host, BROKER_CONFIG.port, BROKER_CONFIG.keepalive)
        print(f"[edge-connect-call] rc={rc}")
        self.client.loop_start()
        if not self._connected.wait(timeout=8):
            raise RuntimeError("Edge gateway failed to connect to MQTT broker")
        if not self._subscribed.wait(timeout=8):
            raise RuntimeError("Edge gateway failed to subscribe to command topics")

    def stop(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()

    def heartbeat_tick(self) -> bool:
        with self._lock:
            return self.runtime.heartbeat_tick()

    def _on_connect(self, client: mqtt.Client, _userdata: Any, _flags: Any, reason_code: Any, _properties: Any) -> None:
        print(f"[edge-connect] reason={reason_code}")
        client.subscribe([(policy.topic, policy.qos) for policy in COMMAND_TOPIC_POLICIES])
        self._connected.set()

    def _on_disconnect(self, _client: mqtt.Client, _userdata: Any, _flags: Any, reason_code: Any, _properties: Any) -> None:
        print(f"[edge-disconnect] reason={reason_code}")

    def _on_subscribe(
        self,
        _client: mqtt.Client,
        _userdata: Any,
        _mid: int,
        reason_code_list: Any,
        _properties: Any,
    ) -> None:
        print(f"[edge-subscribe] reason_codes={reason_code_list}")
        self._subscribed.set()
        if not self._bootstrapped:
            with self._lock:
                self.runtime.handle_command(self._startup_ok())
            self._bootstrapped = True

    def _on_message(self, _client: mqtt.Client, _userdata: Any, message: mqtt.MQTTMessage) -> None:
        decoded = self.codec.decode_payload(message.payload)
        command = self._map_mqtt_command(message.topic, decoded)
        with self._lock:
            self.runtime.handle_command(command)

    def _map_mqtt_command(self, topic: str, decoded: dict[str, Any]):
        edge_commands_module = sys.modules["edge_commands"]
        corr_id = decoded.get("msg_id")
        payload = decoded.get("payload", {})
        if topic == SIM_CONSTANTS.TOPIC_CMD_MODE:
            requested_mode = payload.get("requested_mode")
            if requested_mode == "MANUAL":
                command = edge_commands_module.request_manual_mode()
            elif requested_mode == "AUTO_LINE":
                command = edge_commands_module.request_auto_line_mode()
            else:
                command = edge_commands_module.invalid_command("unsupported_mode_request")
        elif topic == SIM_CONSTANTS.TOPIC_CMD_MANUAL:
            command = edge_commands_module.manual_drive(
                float(payload.get("linear", 0.0)),
                float(payload.get("angular", 0.0)),
            )
        elif topic == SIM_CONSTANTS.TOPIC_CMD_RESET:
            reset_action = payload.get("reset_action")
            if reset_action == "clear_safe_stop":
                command = edge_commands_module.clear_safe_stop()
            elif reset_action == "estop_reset":
                command = edge_commands_module.estop_reset()
            else:
                command = edge_commands_module.invalid_command("unsupported_reset_action")
        else:
            command = edge_commands_module.invalid_command("unsupported_topic")
        command.corr_id = corr_id
        return command


def _create_operator_client() -> mqtt.Client:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_CONFIG.operator_client_id)
    client.on_connect = lambda _client, _userdata, _flags, reason_code, _properties: print(
        f"[operator-connect] reason={reason_code}"
    )
    client.on_disconnect = lambda _client, _userdata, _flags, reason_code, _properties: print(
        f"[operator-disconnect] reason={reason_code}"
    )
    rc = client.connect(BROKER_CONFIG.host, BROKER_CONFIG.port, BROKER_CONFIG.keepalive)
    print(f"[operator-connect-call] rc={rc}")
    client.loop_start()
    time.sleep(1.0)
    return client


def _publish_and_wait(client: mqtt.Client, topic: str, payload: str, qos: int, retain: bool) -> None:
    client.publish(topic, payload, qos=qos, retain=retain)
    print(f"[operator-publish] topic={topic} qos={qos} retain={retain} payload={payload}")
    time.sleep(1.0)


def _observer_has_topic(observer: ConsoleObserver, topic: str) -> bool:
    return any(actual_topic == topic for actual_topic, _payload in observer.messages)


def main() -> None:
    codec = MqttMessageCodec()
    broker = EmbeddedBroker(BROKER_CONFIG.host, BROKER_CONFIG.port)
    observer = ConsoleObserver(CLIENT_CONFIG.observer_client_id, codec)
    late_observer = ConsoleObserver(CLIENT_CONFIG.late_observer_client_id, codec)
    edge_gateway = EdgeTransportGateway(codec)

    broker.start()
    print(f"[broker-started] host={BROKER_CONFIG.host} port={BROKER_CONFIG.port}")
    time.sleep(1.0)

    try:
        observer.start()
        edge_gateway.start()
        time.sleep(1.0)

        operator = _create_operator_client()
        try:
            _publish_and_wait(
                operator,
                SIM_CONSTANTS.TOPIC_CMD_MODE,
                codec.encode_mode_command(requested_mode="MANUAL", corr_id="op-mode-001"),
                qos=1,
                retain=False,
            )
            _publish_and_wait(
                operator,
                SIM_CONSTANTS.TOPIC_CMD_MANUAL,
                codec.encode_manual_command(linear=0.2, angular=0.0, corr_id="op-manual-001"),
                qos=1,
                retain=False,
            )

            operator.loop_stop()
            operator.disconnect()
            time.sleep(0.5)

            late_observer.start()
            time.sleep(0.5)

            operator = _create_operator_client()
            _publish_and_wait(
                operator,
                SIM_CONSTANTS.TOPIC_CMD_MODE,
                codec.encode_mode_command(requested_mode="UNSUPPORTED_MODE", corr_id="op-mode-002"),
                qos=1,
                retain=False,
            )

            print("[transport] advancing edge heartbeat to demonstrate degraded behavior")
            for _ in range(3):
                edge_gateway.heartbeat_tick()
                time.sleep(0.5)
        finally:
            operator.loop_stop()
            operator.disconnect()

        retained_status_ok = _observer_has_topic(late_observer, SIM_CONSTANTS.TOPIC_STATE_STATUS)
        audit_seen = _observer_has_topic(observer, SIM_CONSTANTS.TOPIC_EVENT_AUDIT)
        heartbeat_seen = _observer_has_topic(observer, SIM_CONSTANTS.TOPIC_HEALTH_HEARTBEAT)
        alarm_seen = _observer_has_topic(observer, SIM_CONSTANTS.TOPIC_EVENT_ALARM)

        print("transport_summary")
        print(f"observer_messages={len(observer.messages)}")
        print(f"late_observer_messages={len(late_observer.messages)}")
        print(f"retained_status_ok={retained_status_ok}")
        print(f"audit_seen={audit_seen}")
        print(f"heartbeat_seen={heartbeat_seen}")
        print(f"alarm_seen={alarm_seen}")
        print(f"edge_state={edge_gateway.runtime.state}")
    finally:
        late_observer.stop()
        observer.stop()
        edge_gateway.stop()
        broker.stop()


if __name__ == "__main__":
    main()
