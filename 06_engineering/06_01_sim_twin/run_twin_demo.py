from __future__ import annotations

import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from twin_runtime import TwinRuntime
from twin_scenarios import run_basic_demo


def main() -> None:
    runtime = TwinRuntime()
    print("AGV Denford functional twin demo")
    run_basic_demo(runtime)
    print(f"final_state={runtime.state.value}")
    print(f"published_messages={len(runtime.publisher.messages)}")


if __name__ == "__main__":
    main()
