# Stage 7D.1 Report

## Stage ID and name
- Stage ID: Stage 7D.1
- Stage name: UI corrective polish + manual QA clarity

## Objective
- Keep the existing Stage 7D human UI functionally intact while making it safer for real demo use: no horizontal page breakage on long live/debug messages, less developer language on the main screen, clearer operator flow, and clearer accepted vs rejected command outcomes.

## Input context used
- Existing Stage 7D UI in `06_engineering/06_08_ui/`
- Existing backend REST + WebSocket path in `06_engineering/06_04_backend/`
- Existing Stage 7 integration and Stage 7B polished demo contours
- User-confirmed UX direction: calm, intuitive, child-readable, minimalistic, stylish, ergonomic

## Files created
- `06_engineering/06_08_ui/src/lib/presenters.ts`
- `99_reports/execution/STAGE_07D1_REPORT.md`

## Files updated
- `06_engineering/06_08_ui/src/components/dashboard-header.tsx`
- `06_engineering/06_08_ui/src/components/control-panel.tsx`
- `06_engineering/06_08_ui/src/components/record-list.tsx`
- `06_engineering/06_08_ui/src/components/live-updates-panel.tsx`
- `06_engineering/06_08_ui/src/App.tsx`
- `06_engineering/06_08_ui/src/hooks/use-dashboard.ts`
- `06_engineering/06_08_ui/src/index.css`
- `06_engineering/06_08_ui/ui_demo_walkthrough.md`
- `06_engineering/06_08_ui/ui_test_plan.md`
- `99_reports/execution/MASTER_EXECUTION_REPORT.md`

## UX polish summary
- The main screen now explains the current state in plain language instead of mostly exposing raw enums.
- The top hero now answers three human questions immediately:
  - what state the system is in;
  - what the system is doing now;
  - what the operator should do next.
- The control card now explains the intended flow: choose mode, then send manual motion, then observe the result.
- The UI now surfaces the latest command outcome as one of `idle`, `dispatched`, `accepted`, or `rejected`, with a readable explanation instead of forcing the user to parse raw payloads.

## Layout bug fix summary
- Added `overflow-x-hidden` at page/root level so the page itself no longer grows horizontally from long payloads.
- Added `min-w-0` and `overflow-hidden` to the cards and grid surfaces that previously allowed uncontrolled width growth.
- Moved raw JSON into expandable `details` sections instead of rendering it directly as the main content.
- Raw payloads and raw live frames now use controlled debug rendering:
  - `overflow-x-auto`
  - `whitespace-pre-wrap`
  - `break-words`
- The live updates panel now has a controlled vertical scroll region and no longer dominates the full page width.

## Manual QA clarity summary
- Main state/status labels are now translated into human-oriented explanations such as “Готов к команде”, “Ручное управление активно”, and “Связь потеряна, режим деградации”.
- Rejected and degraded outcomes are explained in plain language rather than only by tokens like `unsupported_mode_request` or `DISCONNECTED_DEGRADED`.
- The UI now makes the command semantics clearer:
  - mode command first;
  - manual command second;
  - reset path only when appropriate;
  - observe outcome in events/live activity.
- Compact human-readable event summaries are shown first, while raw debug JSON is preserved only as secondary details.
- `ui_demo_walkthrough.md` and `ui_test_plan.md` now explicitly describe the main screen and the intended operator flow for manual QA.

## Validation performed
- Static/UI checks:
  - `python3 -m py_compile 06_engineering/06_08_ui/ui_demo_stack.py` passed.
  - `npm run build` in `06_engineering/06_08_ui/` passed.
- UI runtime checks:
  - `python3 06_engineering/06_08_ui/ui_demo_stack.py` passed.
  - `npm run dev -- --host 127.0.0.1 --port 5173` passed.
  - `curl -sSI http://127.0.0.1:5173` returned `200 OK`.
  - `curl -sS http://127.0.0.1:5173` returned the expected Vite/React HTML shell.
  - `node ui_smoke.mjs` passed with:
    - `initial_state=IDLE`
    - `mode_published=true`
    - `manual_published=true`
    - `commands_seen=2`
    - `events_seen=5`
    - `telemetry_seen=1`
    - `live_frames=9`
    - `final_state=MANUAL`
- Regression checks:
  - `python3 06_engineering/06_01_sim_twin/run_stage2_scenarios.py` passed with `summary: passed=8 total=8`.
  - `python3 06_engineering/06_02_edge/edge_demo_runner.py` passed.
  - `python3 06_engineering/06_03_transport/mqtt_transport_runner.py` passed.
  - `python3 06_engineering/06_04_backend/backend_demo_runner.py` passed.
  - `python3 06_engineering/06_05_operator/operator_demo_runner.py` passed.
  - `python3 06_engineering/06_06_integration/integration_runner.py` passed with `summary: passed=10 total=10`.
  - `python3 06_engineering/06_07_polish/demo_runner.py` passed and reached `demo_final_summary`.
- Width-safety validation:
  - Verified in code that long raw messages are now contained by `overflow-x-auto`, `whitespace-pre-wrap`, `break-words`, `min-w-0`, and `overflow-x-hidden`.
  - No automated screenshot/browser-layout assertion was added; this remains a manual QA check rather than a visual regression harness.

## Risks
- Browser-level visual regression is still manual; no screenshot automation or DOM-layout assertion was added.
- The UI is now much clearer, but some backend-origin terms such as `MQTT ingest` and `command bridge` still remain on secondary surfaces for engineering honesty.
- Stage 7D.1 improves demo ergonomics, not production UX completeness.

## Deviations
- No backend protocol changes were introduced because the existing REST + WebSocket path was already sufficient.
- No heavy frontend library was added beyond the existing React + Vite + shadcn/ui-style direction.
- No archive-heavy zones were touched.

## Required / Done / Not done / Why
- Required: stop long live/debug messages from widening cards and the page.
  - Done: controlled overflow and width constraints were added.
- Required: make the main screen more understandable to a non-developer.
  - Done: human-readable state stories and next-step guidance were added.
- Required: make command semantics and acceptance/rejection flow clearer.
  - Done: the controls now use step-based guidance and an explicit command outcome area.
- Required: move raw JSON to a secondary/debug surface.
  - Done: raw payloads and live frames now sit under expandable details.
- Required: update walkthrough/test-plan docs for manual QA.
  - Done: both docs were updated.
- Required: keep the existing architecture and backend protocol.
  - Done: REST + WebSocket remain unchanged from the UI point of view.
- Required: verify that UI launches and that earlier stages still work.
  - Done: UI and Stage 2–7B regression paths were re-run successfully.
- Not done: screenshot-level automated visual QA.
  - Why: outside the scope of this corrective polish stage and not required to keep the UI demo path honest.

## Sanitary Check
- No repo clutter was intentionally introduced.
- New and updated files are limited to `06_engineering/06_08_ui/` and `99_reports/execution/`.
- File names remain explicit and stage-scoped.
- Generated `dist/` and `__pycache__/` artifacts were removed after validation.
- Stage 7D UI still launches.
- Stage 7 integration runner still works.
- Stage 6 operator demo still works.
- Stage 5 backend demo still works.
- Stage 4 transport demo still works.
- Stage 3 edge demo still works.
- Stage 2 scenarios still pass.

## READY TO CLOSE?
- YES

## Reasoned recommendation
- Stage 7D.1 can be closed as a successful corrective UI polish pass.
- Do not move to hardware phase implicitly. The next step should only be opened explicitly, with the current UI positioned honestly as a software-only operator/demo surface.
