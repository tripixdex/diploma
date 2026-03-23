from __future__ import annotations

import asyncio
import importlib.util
import os
import socket
import signal
import sys
import threading
import time
from pathlib import Path
from typing import Any

from amqtt.broker import Broker
import uvicorn


def _load_module(module_name: str, module_path: Path) -> Any:
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module {module_name} from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class EmbeddedBroker:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._broker: Broker | None = None
        self._ready = threading.Event()
        self._startup_error: Exception | None = None

    def start(self) -> None:
        def _run() -> None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._loop = loop
            config = {
                "listeners": {
                    "default": {"type": "tcp", "bind": f"{self.host}:{self.port}"}
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


class UvicornThread:
    def __init__(self, app: Any, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.app = app
        self._thread: threading.Thread | None = None
        self.server = uvicorn.Server(
            uvicorn.Config(app, host=host, port=port, log_level="warning")
        )

    def start(self) -> None:
        def _run() -> None:
            asyncio.run(self.server.serve())

        self._thread = threading.Thread(target=_run, daemon=True)
        self._thread.start()
        deadline = time.time() + 8
        while time.time() < deadline and not self.server.started:
            time.sleep(0.1)
        if not self.server.started:
            raise RuntimeError("Backend HTTP server failed to start")

    def stop(self) -> None:
        self.server.should_exit = True
        if self._thread is not None:
            self._thread.join(timeout=5)


def _can_bind(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
        except OSError:
            return False
    return True


def _select_broker_port(default_port: int) -> tuple[int, str]:
    host = "127.0.0.1"
    if _can_bind(host, default_port):
        return default_port, "default"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        selected_port = sock.getsockname()[1]
    return selected_port, f"fallback_from_{default_port}"


def main() -> None:
    selected_port, selection_mode = _select_broker_port(18884)
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
