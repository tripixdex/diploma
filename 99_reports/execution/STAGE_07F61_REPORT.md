# Stage 07F.6.1 Report

## Stage ID and name
- Stage ID: Sprint 7F.6.1
- Stage name: Canonical Software Baseline Hardening

## Objective
- Remove reviewer confusion around overlapping runtime entrypoints.
- Fix one authoritative software-only baseline path.
- Fix one authoritative health-check / verification path.
- Keep the scope software-only, honest, and unchanged in capability.

## Input context used
- Sprint brief for Sprint 7F.6.1.
- [README.md](/Users/vladgurov/Desktop/study/7sem/diploma/README.md)
- [SOFTWARE_RUNTIME_BASELINE.md](/Users/vladgurov/Desktop/study/7sem/diploma/SOFTWARE_RUNTIME_BASELINE.md)
- [TOP_LEVEL_TRUTH_BASELINE.md](/Users/vladgurov/Desktop/study/7sem/diploma/TOP_LEVEL_TRUTH_BASELINE.md)
- [MASTER_EXECUTION_REPORT.md](/Users/vladgurov/Desktop/study/7sem/diploma/99_reports/execution/MASTER_EXECUTION_REPORT.md)
- Runtime entrypoints:
  - [integration_runner.py](/Users/vladgurov/Desktop/study/7sem/diploma/06_engineering/06_06_integration/integration_runner.py)
  - [demo_runner.py](/Users/vladgurov/Desktop/study/7sem/diploma/06_engineering/06_07_polish/demo_runner.py)
  - [ui_demo_stack.py](/Users/vladgurov/Desktop/study/7sem/diploma/06_engineering/06_08_ui/ui_demo_stack.py)

## Files created
- [SOFTWARE_BASELINE_RUNBOOK.md](/Users/vladgurov/Desktop/study/7sem/diploma/SOFTWARE_BASELINE_RUNBOOK.md)
- [SOFTWARE_BASELINE_MANIFEST.md](/Users/vladgurov/Desktop/study/7sem/diploma/SOFTWARE_BASELINE_MANIFEST.md)
- [STAGE_07F61_REPORT.md](/Users/vladgurov/Desktop/study/7sem/diploma/99_reports/execution/STAGE_07F61_REPORT.md)

## Files updated
- [README.md](/Users/vladgurov/Desktop/study/7sem/diploma/README.md)
- [SOFTWARE_RUNTIME_BASELINE.md](/Users/vladgurov/Desktop/study/7sem/diploma/SOFTWARE_RUNTIME_BASELINE.md)
- [TOP_LEVEL_TRUTH_BASELINE.md](/Users/vladgurov/Desktop/study/7sem/diploma/TOP_LEVEL_TRUTH_BASELINE.md)
- [MASTER_EXECUTION_REPORT.md](/Users/vladgurov/Desktop/study/7sem/diploma/99_reports/execution/MASTER_EXECUTION_REPORT.md)

## Canonical baseline summary
- One authoritative full software-only baseline is now fixed:
  - `python3 06_engineering/06_08_ui/ui_demo_stack.py`
- One authoritative verification path is now fixed:
  - `python3 06_engineering/06_06_integration/integration_runner.py`
- Supporting runners remain available, but they are now explicitly marked as supporting/demo/internal rather than baseline-defining.

## Reviewer-safe run path summary
- Canonical start path:
  - start `ui_demo_stack.py`
  - start Vite UI
  - open `http://127.0.0.1:5173`
- Canonical health proof:
  - backend health endpoint responds with `status=ok`
  - integration runner ends with `summary: passed=10 total=10`
- Supporting paths are explicitly downgraded:
  - `demo_runner.py` is a presentation wrapper only
  - backend/operator/transport/twin runners are proof paths only

## Remaining baseline risks
- The canonical baseline still uses a local embedded broker and dev/demo storage, so it must not be described as deployment-ready.
- Supporting runners still exist, so future docs must avoid accidentally promoting them back to peer baselines.
- No cleaner pyproject entry point was added because the active runtime still depends on stage-directory loading with numeric folder names; adding a synthetic launcher here would increase surface area without reducing reviewer ambiguity materially.

## Validation performed
- Audited current entrypoints and top-level runtime docs for ambiguity:
  - `integration_runner.py`
  - `demo_runner.py`
  - `ui_demo_stack.py`
  - `README.md`
  - `SOFTWARE_RUNTIME_BASELINE.md`
- Confirmed the pre-change ambiguity:
  - `SOFTWARE_RUNTIME_BASELINE.md` called the UI path canonical while also giving `integration_runner.py` a quasi-canonical role.
- Created a separate runbook and manifest to freeze:
  - one canonical baseline,
  - one canonical verification path,
  - explicit supporting-only runners.
- Updated top-level docs so the canonical baseline is now easy to find from the repo root.
- Verified the canonical baseline health endpoint:
  - `curl -sS http://127.0.0.1:8011/health`
  - result: `{"status":"ok","storage_mode":"dev-memory","mqtt_bridge_connected":true,"command_bridge_connected":true}`
- Verified the canonical verification path:
  - `python3 06_engineering/06_06_integration/integration_runner.py`
  - result: `summary: passed=10 total=10`
- Verified runtime-state honesty:
  - direct relaunch of `ui_demo_stack.py` hit `127.0.0.1:8011 already in use`
  - `lsof -nP -iTCP:8011 -sTCP:LISTEN` confirmed an existing local Python process was already serving the canonical backend port
  - this is recorded as current local runtime state, not as a baseline-definition error
- No runtime behavior was expanded.
- No hardware-specific code was added.
- No new deployment or hardware claims were introduced.

## Sanitation Check
- No repo clutter introduced beyond the new baseline docs and this report.
- All new/updated files are in correct folders.
- File names remain understandable and reviewer-facing.
- No temp/random files were left.
- No scope expansion happened.
- The canonical baseline is now distinguishable from supporting/demo paths.
- No inflated claims were introduced.

## Prompt Re-Check
- Required:
  - audit entrypoints,
  - define one canonical baseline,
  - define one canonical verification path,
  - create runbook and manifest,
  - update top-level runtime docs,
  - update execution report.
- Done:
  - all of the above.
- Not done:
  - no new pyproject launcher entry point.
- Why:
  - not needed to remove reviewer ambiguity,
  - would add another launch surface instead of reducing them,
  - current folder/package layout makes a synthetic launcher a packaging convenience rather than a clarity win.

## READY TO CLOSE? YES/NO
- YES

## Reasoned recommendation
- Sprint 7F.6.1 can be closed.
- The canonical reviewer-facing baseline should now be referenced through:
  - [SOFTWARE_BASELINE_RUNBOOK.md](/Users/vladgurov/Desktop/study/7sem/diploma/SOFTWARE_BASELINE_RUNBOOK.md)
  - [SOFTWARE_BASELINE_MANIFEST.md](/Users/vladgurov/Desktop/study/7sem/diploma/SOFTWARE_BASELINE_MANIFEST.md)
- Any future sprint must preserve this distinction:
  - one canonical baseline,
  - one canonical verification path,
  - all other runners supporting only.
