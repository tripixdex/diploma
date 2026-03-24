from __future__ import annotations

import asyncio
import importlib.util
import socket
import sys
import threading
import time
from pathlib import Path
from typing import Any

from amqtt.broker import Broker
import uvicorn


def load_module(module_name: str, module_path: Path) -> Any:
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module {module_name} from {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def load_modules(base_dir: Path, module_names: list[str] | tuple[str, ...]) -> dict[str, Any]:
    return {
        module_name: load_module(module_name, base_dir / f"{module_name}.py")
        for module_name in module_names
    }


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
    def __init__(self, app: Any, host: str, port: int, *, log_level: str = "warning") -> None:
        self.host = host
        self.port = port
        self.app = app
        self._thread: threading.Thread | None = None
        self.server = uvicorn.Server(
            uvicorn.Config(app, host=host, port=port, log_level=log_level)
        )

    def start(self) -> None:
        def _run() -> None:
            asyncio.run(self.server.serve())

        self._thread = threading.Thread(target=_run, daemon=True)
        self._thread.start()
        wait_for(lambda: self.server.started, timeout=8.0)
        if not self.server.started:
            raise RuntimeError("Backend HTTP server failed to start")

    def stop(self) -> None:
        self.server.should_exit = True
        if self._thread is not None:
            self._thread.join(timeout=5)


def wait_for(predicate: Any, *, timeout: float = 8.0, step: float = 0.1) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return True
        time.sleep(step)
    return False


def can_bind(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind((host, port))
        except OSError:
            return False
    return True


def select_port(host: str, default_port: int) -> tuple[int, str]:
    if can_bind(host, default_port):
        return default_port, "default"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        selected_port = sock.getsockname()[1]
    return selected_port, f"fallback_from_{default_port}"
