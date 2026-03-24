from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path


EDGE_DIR = Path(__file__).resolve().parents[1] / "06_engineering" / "06_02_edge"
if str(EDGE_DIR) not in sys.path:
    sys.path.insert(0, str(EDGE_DIR))

from edge_commands import clear_safe_stop, request_manual_mode, startup_ok
from edge_runtime import EdgeRuntime, InMemoryEdgeAdapter


class EdgeRuntimeRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.adapter = InMemoryEdgeAdapter()
        self.runtime = EdgeRuntime(adapter=self.adapter)

    def test_valid_core_transition_to_manual(self) -> None:
        self.assertTrue(self._call(self.runtime.handle_command, startup_ok()))
        self.assertTrue(self._call(self.runtime.handle_command, request_manual_mode()))
        self.assertEqual(self.runtime.state, "MANUAL")

    def test_illegal_transition_is_rejected_and_state_is_unchanged(self) -> None:
        self._call(self.runtime.handle_command, startup_ok())
        self._call(self.runtime.handle_command, request_manual_mode())

        accepted = self._call(self.runtime.handle_command, clear_safe_stop())

        self.assertFalse(accepted)
        self.assertEqual(self.runtime.state, "MANUAL")
        self.assertTrue(
            any(
                record.kind == "audit"
                and record.accepted is False
                and record.payload.get("reason") == "illegal_transition"
                for record in self.adapter.records
            )
        )

    def test_heartbeat_timeout_triggers_degraded_state(self) -> None:
        self._call(self.runtime.handle_command, startup_ok())
        self._call(self.runtime.handle_command, request_manual_mode())

        self.assertFalse(self._call(self.runtime.heartbeat_tick))
        self.assertFalse(self._call(self.runtime.heartbeat_tick))
        accepted = self._call(self.runtime.heartbeat_tick)

        self.assertTrue(accepted)
        self.assertEqual(self.runtime.state, "DISCONNECTED_DEGRADED")

    def test_prolonged_disconnect_escalates_to_safe_stop(self) -> None:
        self._call(self.runtime.handle_command, startup_ok())
        self._call(self.runtime.handle_command, request_manual_mode())

        self._call(self.runtime.heartbeat_tick)
        self._call(self.runtime.heartbeat_tick)
        self._call(self.runtime.heartbeat_tick)

        self.assertEqual(self.runtime.state, "DISCONNECTED_DEGRADED")
        self.assertFalse(self._call(self.runtime.heartbeat_tick))
        accepted = self._call(self.runtime.heartbeat_tick)

        self.assertTrue(accepted)
        self.assertEqual(self.runtime.state, "SAFE_STOP")

    def _call(self, fn, *args):
        with contextlib.redirect_stdout(io.StringIO()):
            return fn(*args)


if __name__ == "__main__":
    unittest.main()
