# Evidence Index

## Purpose
This pack shows what the current software-only MVP actually proves, where the proof lives, and how to verify that a saved artifact is good enough for reviewer use.

## Reviewer 5-Minute Path
1. Read `scenario_to_artifact_matrix.md`.
2. Open `artifacts/logs/20260326T001703+0300__integration_full_chain.log`.
3. Open `artifacts/ui/20260326T001703+0300__ui_proof_summary.md`.
4. Open `artifacts/summaries/20260326T001703+0300__polished_demo_summary.log`.

## Mandatory Scenario Set
| Scenario ID | Scenario | Why It Matters | Primary Proof Artifact | Status |
| --- | --- | --- | --- | --- |
| EVI-001 | Command truth-loop | Shows that a valid operator command really traverses the full software chain. | `artifacts/logs/20260326T001703+0300__integration_full_chain.log` | PASS |
| EVI-002 | Invalid input rejection | Shows that unsupported input is rejected, not silently accepted. | `artifacts/logs/20260326T001703+0300__integration_full_chain.log` | PASS |
| EVI-003 | Degraded -> safe-stop behavior | Shows heartbeat loss causes degraded handling and then safe-stop escalation in software. | `artifacts/logs/20260326T001703+0300__integration_full_chain.log` | PASS |
| EVI-004 | Full-chain integration path | Shows the canonical software-only contour works end to end. | `artifacts/logs/20260326T001703+0300__integration_full_chain.log` | PASS |
| EVI-005 | UI operator/manual-QA path | Shows the browser-facing path is alive, readable, and command-capable over REST + WebSocket. | `artifacts/ui/20260326T001703+0300__ui_proof_summary.md` | PASS |
| EVI-006 | Frozen software-only MVP boundary | Shows the demo package still limits claims to software-only MVP. | `artifacts/summaries/20260326T001703+0300__polished_demo_summary.log` | PASS |

## Artifact Layout
- `artifacts/logs/`
  - compact runner logs with direct success/failure-bearing lines
- `artifacts/http_ws/`
  - compact HTTP availability and backend health responses
- `artifacts/summaries/`
  - short run summaries and boundary/freeze outputs
- `artifacts/ui/`
  - UI-specific proof artifacts and operator-facing smoke summaries
- `artifacts/legacy_pre_7F63/`
  - older unstructured artifacts kept only for traceability, not as the preferred provenance baseline

## What Good Proof Looks Like
- `integration_full_chain.log` ends with `summary: passed=10 total=10`.
- The same log includes explicit rejection evidence for invalid input.
- The same log includes `final_state=SAFE_STOP` and degraded/safe-stop alarm details.
- `ui_http_head.txt` starts with `HTTP/1.1 200 OK`.
- `backend_health.json` includes `"status":"ok"`.
- `ui_smoke_output.txt` shows `mode_published: true`, `manual_published: true`, `telemetry_seen >= 1`, and `live_frames >= 3`.
- `polished_demo_summary.log` ends with `software_mvp_frozen=true` and `claims_limited_to=software_only_contour`.

## What Failure Looks Like
- No `summary: passed=10 total=10` in the integration artifact.
- UI HTTP artifact is not `200 OK`.
- Backend health does not report `status=ok`.
- UI smoke summary shows `mode_published=false`, `manual_published=false`, `telemetry_seen=0`, or `live_frames < 3`.
- Boundary artifact implies hardware or deployment proof rather than software-only limitation.

## Most Useful Artifacts
- `artifacts/logs/20260326T001703+0300__integration_full_chain.log`
- `artifacts/logs/20260326T001703+0300__backend_demo_ingest.log`
- `artifacts/ui/20260326T001703+0300__ui_proof_summary.md`
- `artifacts/ui/20260326T001703+0300__ui_smoke_output.txt`
- `artifacts/http_ws/20260326T001703+0300__backend_health.json`
- `artifacts/http_ws/20260326T001703+0300__ui_http_head.txt`
- `artifacts/summaries/20260326T001703+0300__polished_demo_summary.log`

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
2. `artifacts/logs/20260326T001703+0300__integration_full_chain.log`
3. `artifacts/ui/20260326T001703+0300__ui_proof_summary.md`
