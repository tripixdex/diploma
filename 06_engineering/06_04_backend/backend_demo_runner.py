from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

import paho.mqtt.client as mqtt
from fastapi.testclient import TestClient

from backend_app import build_backend_context, create_backend_app
from backend_config import BROKER_CONFIG, MqttMessageCodec, SIM_CONSTANTS


def _load_runtime_bootstrap():
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

EmbeddedBroker = _load_runtime_bootstrap().EmbeddedBroker


def _publish(client: mqtt.Client, topic: str, payload: str, qos: int = 1, retain: bool = False) -> None:
    client.publish(topic, payload, qos=qos, retain=retain)
    print(f"[backend-demo-publish] topic={topic} retain={retain}")
    time.sleep(0.5)


def main() -> None:
    codec = MqttMessageCodec()
    broker = EmbeddedBroker(BROKER_CONFIG.host, BROKER_CONFIG.port)
    broker.start()
    print(f"[backend-demo] broker_started host={BROKER_CONFIG.host} port={BROKER_CONFIG.port}")

    context = build_backend_context()
    app = create_backend_app(context)
    context.mqtt_bridge.start()

    producer = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="agv-denford-backend-demo-producer")
    producer.connect(BROKER_CONFIG.host, BROKER_CONFIG.port, BROKER_CONFIG.keepalive)
    producer.loop_start()

    client = TestClient(app)
    with client.websocket_connect("/ws/live") as websocket:
        print(f"[backend-demo] websocket_handshake={websocket.receive_json()}")

        _publish(
            producer,
            SIM_CONSTANTS.TOPIC_CMD_MODE,
            codec.encode_mode_command(requested_mode="MANUAL"),
        )
        _publish(
            producer,
            SIM_CONSTANTS.TOPIC_EVENT_AUDIT,
            codec.encode_event_message(
                kind="audit",
                mode="MANUAL",
                state="MANUAL",
                payload={"result": SIM_CONSTANTS.AUDIT_RESULT_ACCEPTED, "reason": "backend_demo_ingest"},
                source="edge",
            ),
        )
        _publish(
            producer,
            SIM_CONSTANTS.TOPIC_STATE_STATUS,
            codec.encode_event_message(
                kind="status",
                mode="MANUAL",
                state="MANUAL",
                payload={"traction_enabled": True, "transition_reason": "backend_demo_status"},
                source="edge",
            ),
            retain=True,
        )
        _publish(
            producer,
            SIM_CONSTANTS.TOPIC_STATE_TELEMETRY,
            codec.encode_event_message(
                kind="telemetry",
                mode="MANUAL",
                state="MANUAL",
                payload={"linear": 0.2, "angular": 0.0},
                source="edge",
            ),
        )

        live_frame = websocket.receive_json()
        print(f"[backend-demo] websocket_frame={live_frame}")

    health = client.get("/health").json()
    current_status = client.get("/api/status/current").json()
    recent_events = client.get("/api/events/recent").json()
    recent_commands = client.get("/api/commands/recent").json()
    recent_telemetry = client.get("/api/telemetry/recent").json()

    print(f"[backend-demo] health={health}")
    print(f"[backend-demo] current_status={current_status}")
    print(f"[backend-demo] recent_events_count={len(recent_events['events'])}")
    print(f"[backend-demo] recent_commands_count={len(recent_commands['commands'])}")
    print(f"[backend-demo] recent_telemetry_count={len(recent_telemetry['telemetry'])}")

    producer.loop_stop()
    producer.disconnect()
    context.mqtt_bridge.stop()
    broker.stop()


if __name__ == "__main__":
    main()
