from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

from operator_api_client import BackendApiClient
from operator_commands import OperatorCommandPublisher
from operator_client_config import BROKER_CONFIG, MqttMessageCodec
from operator_models import OperatorRunSummary
from operator_ws_client import OperatorWsClient


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


def _load_backend_bundle() -> dict[str, Any]:
    backend_dir = Path(__file__).resolve().parents[1] / "06_04_backend"
    for name in [
        "backend_models",
        "backend_config",
        "backend_storage",
        "backend_ws",
        "backend_command_bridge",
        "backend_mqtt_bridge",
        "backend_api",
    ]:
        _load_module(name, backend_dir / f"{name}.py")
    backend_app = _load_module("backend_app", backend_dir / "backend_app.py")
    return {
        "build_backend_context": backend_app.build_backend_context,
        "create_backend_app": backend_app.create_backend_app,
    }


def _load_transport_bundle() -> dict[str, Any]:
    transport_dir = Path(__file__).resolve().parents[1] / "06_03_transport"
    for name in ["mqtt_client_config", "mqtt_message_codec"]:
        _load_module(name, transport_dir / f"{name}.py")
    transport_runner = _load_module("mqtt_transport_runner", transport_dir / "mqtt_transport_runner.py")
    return {
        "EdgeTransportGateway": transport_runner.EdgeTransportGateway,
    }


def main() -> None:
    codec = MqttMessageCodec()
    backend_bundle = _load_backend_bundle()
    transport_bundle = _load_transport_bundle()
    broker = EmbeddedBroker(BROKER_CONFIG.host, BROKER_CONFIG.port)
    broker.start()
    print(f"[operator-demo] broker_started host={BROKER_CONFIG.host} port={BROKER_CONFIG.port}")

    edge_gateway = transport_bundle["EdgeTransportGateway"](codec)
    backend_context = backend_bundle["build_backend_context"]()
    app = backend_bundle["create_backend_app"](backend_context)
    api_test_client = TestClient(app)
    api_client = BackendApiClient(api_test_client)
    ws_client = OperatorWsClient(api_test_client)
    command_publisher = OperatorCommandPublisher(codec)

    try:
        edge_gateway.start()
        backend_context.mqtt_bridge.start()
        time.sleep(1.0)

        initial_status = api_client.get_current_status()
        initial_events = api_client.get_recent_events()
        initial_telemetry = api_client.get_recent_telemetry()
        print(f"[operator-demo] initial_status={initial_status}")
        print(f"[operator-demo] initial_events={len(initial_events)} initial_telemetry={len(initial_telemetry)}")

        command_publisher.start()

        def _exercise_operator_path() -> None:
            command_publisher.send_mode_command("MANUAL", corr_id="operator-mode-001")
            command_publisher.send_manual_command(0.15, 0.0, corr_id="operator-manual-001")
            command_publisher.send_reset_command("clear_safe_stop", state="MANUAL", corr_id="operator-reset-001")
            for _ in range(3):
                edge_gateway.heartbeat_tick()
                time.sleep(0.5)

        live_frames = ws_client.capture_frames(frame_limit=14, on_connected=_exercise_operator_path)

        final_status = api_client.get_current_status()
        recent_events = api_client.get_recent_events()
        recent_commands = api_client.get_recent_commands()
        recent_telemetry = api_client.get_recent_telemetry()
        health = api_client.get_health()

        summary = OperatorRunSummary(
            initial_status=initial_status,
            final_status=final_status,
            event_count=len(recent_events),
            telemetry_count=len(recent_telemetry),
            command_count=len(recent_commands),
            live_frame_count=len(live_frames),
        )

        print(f"[operator-demo] health={health}")
        print(f"[operator-demo] final_status={final_status}")
        print(f"[operator-demo] recent_events_count={summary.event_count}")
        print(f"[operator-demo] recent_commands_count={summary.command_count}")
        print(f"[operator-demo] recent_telemetry_count={summary.telemetry_count}")
        print(f"[operator-demo] live_frames={summary.live_frame_count}")
        if live_frames:
            print(f"[operator-demo] first_live_frame={live_frames[0]}")
            print(f"[operator-demo] last_live_frame={live_frames[-1]}")
    finally:
        command_publisher.stop()
        backend_context.mqtt_bridge.stop()
        edge_gateway.stop()
        broker.stop()


if __name__ == "__main__":
    main()
