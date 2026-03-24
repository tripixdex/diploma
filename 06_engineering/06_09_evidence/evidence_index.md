# Evidence Index

## Purpose
This pack shows what the current software-only MVP actually proves, where the proof lives, and where the proof is still limited.

## Strongest Evidence
- Full-chain local integration loop:
  `operator -> backend -> MQTT -> edge -> MQTT -> backend -> operator`
- Invalid command rejection with explicit audit evidence.
- Heartbeat timeout escalation into degraded and then safe-stop behavior.
- Human UI path over the existing backend REST and WebSocket contour.
- Frozen MVP boundary wording that limits claims to software-only proof.

## What Was Tested
- Contract-aligned command truth-loop.
- Invalid input rejection.
- Degraded to safe-stop behavior on lost heartbeat.
- Full-chain integration path.
- UI operator/manual-QA path.
- Frozen software-only MVP boundary.

## Where To Look
- Scenario matrix:
  `scenario_to_artifact_matrix.md`
- Claims-to-evidence mapping:
  `software_only_claims_evidence_map.md`
- Evidence collection rules:
  `evidence_collection_policy.md`
- Compact saved artifacts:
  `artifacts/`

## Most Useful Artifacts
- `artifacts/integration_full_chain.log`
- `artifacts/backend_demo_ingest.log`
- `artifacts/ui_smoke_summary.json`
- `artifacts/ui_http_head.txt`
- `artifacts/backend_health.json`
- `artifacts/polished_demo_summary.log`

## Honest Limits
- No hardware evidence.
- No GPIO or board-binding evidence.
- No Webots evidence.
- No PostgreSQL runtime evidence.
- No Docker deployment evidence.
- No deployment-grade Mosquitto evidence.
- No real AGV safety proof.
- Current operating limits are fixed separately in `../06_10_policy/pre_hardware_operating_policy.md`.

## Reviewer Shortcut
If you only read three files:
1. `scenario_to_artifact_matrix.md`
2. `software_only_claims_evidence_map.md`
3. `artifacts/integration_full_chain.log`
