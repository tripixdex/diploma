# Stage 07F.3 Report

## Stage ID and Name
- Stage ID: `Sprint 7F.3`
- Stage name: `Runtime / Bootstrap Cleanup`

## Objective
- Reduce duplicated bootstrap/runtime assembly logic in the canonical software-only contour.
- Make entrypoints thinner and less fragile without changing frozen MVP scope or protocol semantics.

## Input Context Used
- Sprint 7F.3 task constraints from the user prompt.
- Existing canonical runtime entrypoints:
  - `06_engineering/06_06_integration/integration_runner.py`
  - `06_engineering/06_08_ui/ui_demo_stack.py`
  - `06_engineering/06_03_transport/mqtt_transport_runner.py`
  - `06_engineering/06_05_operator/operator_demo_runner.py`
  - `06_engineering/06_04_backend/backend_demo_runner.py`
  - `06_engineering/06_07_polish/demo_runner.py`
- Existing runtime-facing docs:
  - `README.md`
  - `SOFTWARE_RUNTIME_BASELINE.md`
  - `99_reports/execution/MASTER_EXECUTION_REPORT.md`

## Files Created
- `06_engineering/runtime_bootstrap.py`

## Files Updated
- `06_engineering/06_03_transport/mqtt_client_config.py`
- `06_engineering/06_03_transport/mqtt_transport_runner.py`
- `06_engineering/06_04_backend/backend_config.py`
- `06_engineering/06_04_backend/backend_demo_runner.py`
- `06_engineering/06_05_operator/operator_client_config.py`
- `06_engineering/06_05_operator/operator_demo_runner.py`
- `06_engineering/06_06_integration/integration_runner.py`
- `06_engineering/06_07_polish/demo_runner.py`
- `06_engineering/06_08_ui/ui_demo_stack.py`
- `README.md`
- `SOFTWARE_RUNTIME_BASELINE.md`
- `99_reports/execution/MASTER_EXECUTION_REPORT.md`

## Bootstrap Cleanup Summary
- Added one small shared runtime assembly utility: `06_engineering/runtime_bootstrap.py`.
- Centralized repeated logic for:
  - path-based module loading,
  - embedded local MQTT broker startup/shutdown,
  - local Uvicorn server thread startup/shutdown,
  - broker port fallback selection.
- Reduced duplicated bootstrap code in the canonical entrypoints instead of copying the same classes and helper functions in multiple scripts.
- Fixed a real fragility bug in broker port probing: the old free-port check could incorrectly accept an occupied default port on the current host OS.

## Shared Runtime Assembly Summary
- `integration_runner.py` now reuses shared broker/loader/port-selection utilities instead of keeping local copies.
- `ui_demo_stack.py` now reuses shared broker, Uvicorn thread, module loader, and broker-port selection.
- `mqtt_transport_runner.py`, `operator_demo_runner.py`, and `backend_demo_runner.py` now reuse the shared embedded broker implementation.
- `mqtt_client_config.py`, `backend_config.py`, and `operator_client_config.py` now reuse the shared module loader instead of each carrying their own copy.
- `demo_runner.py` now reuses the shared module loader when dispatching into the Stage 7 integration contour.

## Remaining Fragility Risks
- The active stage directories still use numeric names, so path-based dynamic loading is still required; this sprint reduced duplication but did not convert the repo into a normal importable package tree.
- Standalone stage demo scripts still remain separate entrypoints rather than a single unified CLI.
- Stage 4/5/6 standalone demos still mostly rely on the configured broker port and are less adaptive than the canonical integration/UI entrypoints.
- The contour remains local software-only runtime assembly, not deployment-grade bootstrap.

## Validation Performed
- `python3 -m py_compile 06_engineering/runtime_bootstrap.py 06_engineering/06_03_transport/*.py 06_engineering/06_04_backend/*.py 06_engineering/06_05_operator/*.py 06_engineering/06_06_integration/*.py 06_engineering/06_07_polish/*.py 06_engineering/06_08_ui/ui_demo_stack.py`
- `python3 06_engineering/06_06_integration/integration_runner.py`
  - Result: `summary: passed=10 total=10`
  - Additional evidence: broker fallback now worked cleanly when `18884` was already occupied.
- `python3 06_engineering/06_07_polish/demo_runner.py`
  - Result: completed successfully with `demo_final_summary`
- `python3 06_engineering/06_08_ui/ui_demo_stack.py`
  - Result: stack started successfully and backend health answered.
- `curl -sS http://127.0.0.1:8011/health`
  - Result: `{"status":"ok","storage_mode":"dev-memory","mqtt_bridge_connected":true,"command_bridge_connected":true}`
- No new hardware-specific, deployment-grade, or protocol-expansion claims were introduced.

## Sanitation Check
- No repo clutter was intentionally introduced.
- All changed files remain in correct folders.
- File names remain understandable.
- Temporary validation artifacts were not kept as project files.
- Pre-existing root `.DS_Store` clutter and the existing UI `dist/` artifact remain outside this sprint's cleanup scope.
- Runtime behavior remains software-only and honest.
- Scope stayed within bootstrap/runtime cleanup; no new business features were added.

## Prompt Re-Check
- Required:
  - audit duplicated startup/bootstrap logic;
  - add one shared bootstrap utility layer;
  - thin entrypoints;
  - preserve frozen behavior;
  - update runtime-facing docs if needed;
  - update `MASTER_EXECUTION_REPORT.md`;
  - validate canonical entrypoints and keep honesty.
- Done:
  - duplicated broker/Uvicorn/module-loader/port-selection logic was audited and reduced;
  - shared utility `06_engineering/runtime_bootstrap.py` was created;
  - canonical entrypoints were made thinner;
  - docs were updated in `README.md` and `SOFTWARE_RUNTIME_BASELINE.md`;
  - `MASTER_EXECUTION_REPORT.md` was aligned to Sprint 7F.3;
  - validation confirmed no regression in the Stage 7 integration path and UI demo stack.
- Not done:
  - no packaging work beyond what Sprint 7F.2 already established;
  - no evidence-pack cleanup;
  - no hardware policy or hardware bootstrap work;
  - no conversion of the whole repo to a normal package/import structure.
- Why:
  - these are outside Sprint 7F.3 scope;
  - the sprint was intentionally limited to narrow runtime/bootstrap hygiene.

## READY TO CLOSE?
- YES

## Reasoned Recommendation
- Sprint 7F.3 can be closed.
- The next step, if needed, should be `Sprint 7F.4` only.
- Use `06_engineering/runtime_bootstrap.py` as the shared runtime assembly source for the canonical software-only contour, but do not oversell it as deployment bootstrap or hardware readiness.
