from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path
from typing import Any


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


def _load_integration_runner() -> Any:
    integration_path = Path(__file__).resolve().parents[1] / "06_06_integration" / "integration_runner.py"
    return _load_module("integration_runner", integration_path)


def main() -> None:
    started_at = time.time()
    print("AGV Denford Stage 7B Demo")
    print("software_only=true")
    print("hardware_binding=false")
    print("primary_target=Raspberry Pi 4")
    print("secondary_portability_target=Orange Pi")
    print("demo_outline")
    print("1. startup")
    print("2. operator visibility")
    print("3. operator command")
    print("4. edge reaction")
    print("5. MQTT transfer")
    print("6. backend persistence")
    print("7. live update")
    print("8. degraded behavior")
    print("9. invalid command rejection")
    print("10. final summary")
    print("demo_execution_begin")

    integration_runner = _load_integration_runner()
    integration_runner.main()

    elapsed = time.time() - started_at
    print("demo_final_summary")
    print("software_mvp_frozen=true")
    print("hardware_specific_code_introduced=false")
    print("claims_limited_to=software_only_contour")
    print(f"elapsed_seconds={elapsed:.2f}")


if __name__ == "__main__":
    main()
