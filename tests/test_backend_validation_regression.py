from __future__ import annotations

import sys
import unittest
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient


BACKEND_DIR = Path(__file__).resolve().parents[1] / "06_engineering" / "06_04_backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from backend_api import build_api_router
from backend_storage import InMemoryBackendStorage


class _FakeCommandBridge:
    def send_mode_command(self, *, requested_mode: str, corr_id: str | None = None) -> dict:
        return {
            "published": True,
            "topic": "agv/denford/v1/cmd/mode",
            "msg_id": "cmd-mode-001",
            "corr_id": corr_id,
            "ack_required": True,
            "requested_mode": requested_mode,
        }

    def send_manual_command(
        self,
        *,
        linear: float,
        angular: float,
        duration_ms: int = 500,
        corr_id: str | None = None,
    ) -> dict:
        return {
            "published": True,
            "topic": "agv/denford/v1/cmd/manual",
            "msg_id": "cmd-manual-001",
            "corr_id": corr_id,
            "ack_required": True,
            "linear": linear,
            "angular": angular,
            "duration_ms": duration_ms,
        }

    def send_reset_command(
        self,
        *,
        reset_action: str,
        state: str,
        corr_id: str | None = None,
    ) -> dict:
        return {
            "published": True,
            "topic": "agv/denford/v1/cmd/reset",
            "msg_id": "cmd-reset-001",
            "corr_id": corr_id,
            "ack_required": True,
            "reset_action": reset_action,
            "state": state,
        }


class BackendValidationRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        app = FastAPI()
        storage = InMemoryBackendStorage()
        app.include_router(
            build_api_router(
                storage,
                lambda: {
                    "status": "ok",
                    "storage_mode": storage.mode,
                    "mqtt_bridge_connected": False,
                    "command_bridge_connected": False,
                },
                _FakeCommandBridge(),
            )
        )
        self.client = TestClient(app)

    def test_invalid_mode_is_rejected_by_backend_validation(self) -> None:
        response = self.client.post("/api/control/mode", json={"requested_mode": "UNSUPPORTED_MODE"})

        self.assertEqual(response.status_code, 422)
        self.assertIn("MANUAL", response.text)

    def test_invalid_manual_range_is_rejected_by_backend_validation(self) -> None:
        response = self.client.post(
            "/api/control/manual",
            json={"linear": 1.0, "angular": 0.0, "duration_ms": 500},
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn("less than or equal to 0.3", response.text)

    def test_illegal_reset_state_pair_is_rejected_by_backend_validation(self) -> None:
        response = self.client.post(
            "/api/control/reset",
            json={"reset_action": "clear_safe_stop", "state": "ESTOP_LATCHED"},
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn("SAFE_STOP", response.text)

    def test_dispatch_is_not_reported_as_acceptance(self) -> None:
        response = self.client.post(
            "/api/control/mode",
            json={"requested_mode": "MANUAL", "corr_id": "truth-loop-001"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["published"])
        self.assertNotIn("accepted", payload)
        self.assertNotIn("rejected", payload)
        self.assertEqual(payload["corr_id"], "truth-loop-001")


if __name__ == "__main__":
    unittest.main()
