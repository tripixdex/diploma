from __future__ import annotations

import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from twin_scenarios import execute_all_mandatory_scenarios


def main() -> None:
    results = execute_all_mandatory_scenarios()
    print("AGV Denford Stage 2 mandatory scenario run")
    passed = 0
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        if result.passed:
            passed += 1
        print(f"[{status}] {result.name}")
        print(f"  expected_transition: {result.expected_transition}")
        print(f"  actual_transition:   {result.actual_transition}")
        print(f"  expected_evidence:   {result.expected_published_evidence}")
        print(f"  actual_evidence:     {result.actual_published_evidence}")
        print(f"  notes:               {result.notes}")
    print(f"summary: passed={passed} total={len(results)}")


if __name__ == "__main__":
    main()
