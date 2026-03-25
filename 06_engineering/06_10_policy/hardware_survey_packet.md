# Hardware Survey Packet

## Mission Status
- The first lab visit is a survey mission only.
- It is not a hardware integration mission.
- It is not a GPIO experiment session.
- It is not a motion-control test session.
- It is not evidence that the project is hardware-ready.

## Mission Objective
- Collect board facts, AGV-side interface facts, lab constraints, and evidence artifacts needed before any honest hardware phase can be opened.
- Return with verified observations and explicitly marked unknowns.
- Prevent unsafe improvisation and premature board-binding claims.

## Packet Contents
- `board_fact_checklist.md`
- `first_lab_data_capture_sheet.md`
- `lab_no_go_actions.md`
- `first_lab_expected_artifacts.md`
- `first_lab_visit_checklist.md`

## Required Mission Outputs
- Exact board identity is captured or explicitly marked unknown.
- Board mounting, connectors, power entry path, and attached interface hardware are photographed and noted.
- AGV-side power, driver, sensor, and ESTOP observations are captured without guessing beyond evidence.
- Allowed and forbidden lab actions are recorded.
- Post-visit unknowns are listed explicitly instead of silently omitted.

## Conduct Rules
- Separate every fact into one of three categories:
  - directly observed,
  - verbally reported,
  - still unknown.
- Photograph first, infer later.
- If power, ESTOP, connector identity, or supervision rules are unclear, stop and document the uncertainty.
- Do not convert a survey visit into an integration attempt.

## Out Of Scope On The First Visit
- Deploying board-specific runtime code.
- Direct GPIO experiments on unknown lines.
- Direct motor-drive commands.
- Sensor excitation or signal injection on unknown interfaces.
- Casual energizing of unknown power paths.
- Any claim that board binding is ready from photos alone.

## Reviewer Note
- This packet exists to make the first lab visit controlled, evidence-driven, and boring.
- If the visit returns without the required facts, the honest result is "hardware phase still blocked".
