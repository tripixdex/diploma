from __future__ import annotations

import importlib.util
import os
import signal
import sys
import threading
import time
from pathlib import Path
from typing import Any

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
UvicornThread = _RUNTIME_BOOTSTRAP.UvicornThread
load_module = _RUNTIME_BOOTSTRAP.load_module
select_port = _RUNTIME_BOOTSTRAP.select_port
_load_module = load_module


def main() -> None:
    selected_port, selection_mode = select_port("127.0.0.1", 18884)
    os.environ["AGV_MQTT_PORT"] = str(selected_port)
    transport_dir = Path(__file__).resolve().parents[1] / "06_03_transport"
    backend_dir = Path(__file__).resolve().parents[1] / "06_04_backend"

    _load_module("mqtt_client_config", transport_dir / "mqtt_client_config.py")
    codec_module = _load_module("mqtt_message_codec", transport_dir / "mqtt_message_codec.py")
    runner_module = _load_module("mqtt_transport_runner", transport_dir / "mqtt_transport_runner.py")

    for name in [
        "backend_models",
        "backend_config",
        "backend_storage",
        "backend_ws",
        "backend_command_bridge",
        "backend_mqtt_bridge",
        "backend_api",
        "backend_app",
    ]:
        _load_module(name, backend_dir / f"{name}.py")

    client_config = sys.modules["mqtt_client_config"]
    backend_app = sys.modules["backend_app"]
    codec = codec_module.MqttMessageCodec()
    broker_config = client_config.BROKER_CONFIG

    broker = EmbeddedBroker(broker_config.host, broker_config.port)
    edge_gateway = runner_module.EdgeTransportGateway(codec)
    backend_context = backend_app.build_backend_context()
    app = backend_app.create_backend_app(backend_context)
    server = UvicornThread(app, host="127.0.0.1", port=8011)

    stop_event = threading.Event()

    def _request_stop(_signum: int, _frame: Any) -> None:
        stop_event.set()

    signal.signal(signal.SIGINT, _request_stop)
    signal.signal(signal.SIGTERM, _request_stop)

    broker.start()
    edge_gateway.start()
    server.start()

    def _heartbeat_loop() -> None:
        while not stop_event.is_set():
            time.sleep(4.0)
            try:
                edge_gateway.heartbeat_tick()
            except Exception as exc:
                print(f"heartbeat_tick_failed={exc}")

    heartbeat_thread = threading.Thread(target=_heartbeat_loop, daemon=True)
    heartbeat_thread.start()

    print("ui_demo_stack_started")
    print(f"broker={broker_config.host}:{broker_config.port}")
    print(f"broker_port_selection={selection_mode}")
    print("backend=http://127.0.0.1:8011")
    print("ws=ws://127.0.0.1:8011/ws/live")
    print("heartbeat_scheduler=enabled")
    print("Start the UI with: cd 06_engineering/06_08_ui && npm run dev -- --host 127.0.0.1 --port 5173")
    print("Press Ctrl+C to stop the stack.")

    try:
        while not stop_event.is_set():
            time.sleep(1.0)
    finally:
        server.stop()
        edge_gateway.stop()
        broker.stop()


if __name__ == "__main__":
    main()
