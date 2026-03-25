# Stage ID and name
Sprint 7F.6.4: Hardware Survey Packet Hardening

## Objective
Harden a reviewer-safe first-lab survey packet so the first honest lab visit remains a controlled fact-collection mission rather than premature hardware integration.

## Input context used
- Existing policy layer in `06_engineering/06_10_policy/`
- Existing top-level truth baseline
- Existing hardware-entry gate wording
- Current sprint constraints: no hardware code, no new features, no runtime changes, no scope expansion

## Files created
- `06_engineering/06_10_policy/hardware_survey_packet.md`
- `06_engineering/06_10_policy/first_lab_data_capture_sheet.md`
- `06_engineering/06_10_policy/board_fact_checklist.md`
- `06_engineering/06_10_policy/lab_no_go_actions.md`
- `06_engineering/06_10_policy/first_lab_expected_artifacts.md`
- `99_reports/execution/STAGE_07F64_REPORT.md`

## Files updated
- `06_engineering/06_10_policy/README.md`
- `06_engineering/06_10_policy/first_lab_visit_checklist.md`
- `06_engineering/06_10_policy/pre_hardware_operating_policy.md`
- `06_engineering/06_10_policy/hardware_entry_gate.md`
- `TOP_LEVEL_TRUTH_BASELINE.md`
- `99_reports/execution/MASTER_EXECUTION_REPORT.md`

## Hardware survey packet summary
- Added a dedicated survey-packet layer for the first lab visit.
- Made the mission explicit: first lab visit equals survey only, not integration.
- Centralized the packet into one readable set:
  - survey packet overview,
  - board-fact checklist,
  - capture sheet,
  - no-go actions,
  - expected artifacts,
  - quick field checklist.

## Board-fact capture summary
- Board capture is now stricter and reviewer-safe.
- The packet requires recording:
  - exact board vendor/model/revision,
  - board photos,
  - connector and header photos,
  - power-entry observations,
  - attached HAT/controller/interface facts,
  - mounting/usage context,
  - whether Orange Pi is actually relevant in the real lab setup.
- Unknown board facts must now be written as unknown, not inferred.

## No-go boundary summary
- Added an explicit no-go document for the first lab visit.
- It now forbids:
  - direct motor/GPIO experiments,
  - unknown-path energizing,
  - ESTOP-bypass behavior,
  - premature pin-mapping claims,
  - board-readiness claims from photos alone,
  - ad-hoc "let's just try" behavior.
- Immediate stop conditions are now written down explicitly.

## Expected first-lab artifact summary
- The packet now requires a concrete return set:
  - board overview and markings photos,
  - connector/header photo set,
  - power and ESTOP observations,
  - motor/driver and sensor-interface notes,
  - signal mapping notes with explicit unknowns,
  - filled data capture sheet,
  - structured unknowns list,
  - procedure-boundary notes.
- Suggested naming is included so returned artifacts are easier to review later.

## Remaining survey risks
- Exact board facts remain unconfirmed until the actual visit happens.
- Real lab procedure constraints may still differ from current assumptions.
- The packet reduces improvisation risk, but it does not itself prove hardware readiness.
- No hardware survey has been performed yet; this sprint hardens preparation only.

## Validation performed
- Reviewed existing policy docs and identified the gap: first-lab intent existed, but the packet was still too loose and easy to interpret as integration preparation.
- Confirmed all requested survey-packet entry docs now exist and are readable:
  - `hardware_survey_packet.md`
  - `first_lab_data_capture_sheet.md`
  - `board_fact_checklist.md`
  - `lab_no_go_actions.md`
  - `first_lab_expected_artifacts.md`
- Confirmed the packet now makes the first-lab mission explicitly survey-only.
- Confirmed no-go actions are explicit.
- Confirmed board-fact checklist is explicit.
- Confirmed expected first-lab artifacts are explicit.
- Confirmed top-level truth remains honest and does not introduce hardware-readiness claims.

## Sanitation Check
- No repo clutter introduced beyond the intended survey-packet and report files.
- All survey-packet files remain inside `06_engineering/06_10_policy/`.
- File names remain understandable and reviewer-safe.
- No temp or random files were left behind.
- No new hardware-readiness or deployment claims were introduced.
- The packet remains survey-only and not integration-ready.

## Prompt Re-Check
- Required:
  - harden a dedicated survey-packet layer,
  - define first-lab mission as survey-only,
  - harden board-fact capture,
  - harden AGV-side survey capture,
  - add explicit no-go boundaries,
  - make the packet reviewer-friendly,
  - keep top-level truth and policy consistent,
  - update stage report and master execution report.
- Done:
  - created all requested survey-packet docs,
  - made the first-lab mission explicitly survey-only,
  - added stricter board and AGV-side capture requirements,
  - added no-go actions and stop conditions,
  - added expected artifact requirements,
  - updated policy and top-level truth for consistency,
  - synchronized `MASTER_EXECUTION_REPORT.md`.
- Not done:
  - no hardware survey execution,
  - no hardware integration,
  - no runtime changes.
- Why:
  - the sprint is preparation and policy hardening only,
  - hardware execution and integration are explicitly outside scope.

## READY TO CLOSE? YES/NO
YES

## Reasoned recommendation
Sprint 7F.6.4 can be closed. The first-lab packet is now explicit enough to constrain the visit into fact collection rather than improvisational integration. The next step, if explicitly opened, should be only the next reviewer-approved sprint; do not jump from this packet directly into hardware implementation claims.
