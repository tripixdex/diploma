from __future__ import annotations

import asyncio
import threading
import time

import paho.mqtt.client as mqtt
from amqtt.broker import Broker
from fastapi.testclient import TestClient

from backend_app import build_backend_context, create_backend_app
from backend_config import BROKER_CONFIG, MqttMessageCodec, SIM_CONSTANTS


class EmbeddedBroker:
    def __init__(self) -> None:
        self._loop = None
        self._thread = None
        self._ready = threading.Event()
        self._broker = None
        self._startup_error = None

    def start(self) -> None:
        def _run() -> None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._loop = loop
            config = {
                "listeners": {
                    "default": {
                        "type": "tcp",
                        "bind": f"{BROKER_CONFIG.host}:{BROKER_CONFIG.port}",
                    }
                },
                "plugins": {
                    "amqtt.plugins.authentication.AnonymousAuthPlugin": {"allow_anonymous": True},
                    "amqtt.plugins.sys.broker.BrokerSysPlugin": {"sys_interval": 0},
                },
            }
            self._broker = Broker(config, loop=loop)
            try:
                loop.run_until_complete(self._broker.start())
                self._ready.set()
                loop.run_forever()
            except Exception as exc:
                self._startup_error = exc
                self._ready.set()
            finally:
                if self._broker is not None:
                    loop.run_until_complete(self._broker.shutdown())
                loop.close()

        self._thread = threading.Thread(target=_run, daemon=True)
        self._thread.start()
        self._ready.wait(timeout=5)
        if self._startup_error is not None:
            raise self._startup_error

    def stop(self) -> None:
        if self._loop is None or self._thread is None:
            return
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join(timeout=5)


def _publish(client: mqtt.Client, topic: str, payload: str, qos: int = 1, retain: bool = False) -> None:
    client.publish(topic, payload, qos=qos, retain=retain)
    print(f"[backend-demo-publish] topic={topic} retain={retain}")
    time.sleep(0.5)


def main() -> None:
    codec = MqttMessageCodec()
    broker = EmbeddedBroker()
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
