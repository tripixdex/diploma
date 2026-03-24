# First Lab Visit Checklist

## Objective
- Collect factual hardware evidence before any hardware-specific implementation claim is made.

## Must Collect
- Board photos:
  - overall board view,
  - readable model markings,
  - connected peripherals if present.
- Connector photos:
  - power connectors,
  - motor/driver connectors,
  - sensor connectors,
  - ESTOP-related connectors or control cabinet interfaces if visible.
- Signal mapping notes:
  - connector names,
  - probable function,
  - unknown pins or lines,
  - direction assumptions clearly marked as unverified until confirmed.
- Power notes:
  - supply values,
  - grounding facts,
  - power sequencing constraints,
  - anything lab staff warns must not be changed.
- ESTOP notes:
  - what is physically wired,
  - what software does not control,
  - what parts of the stop chain remain fully local.
- Interface constraints:
  - voltage levels,
  - communication buses,
  - isolation requirements,
  - access limitations.

## Must Log
- Date, place, and participants.
- Which board was present.
- Which interfaces were physically observed.
- Which facts were confirmed by direct observation.
- Which facts were told verbally and remain not independently verified.
- Which questions remain unresolved after the visit.

## What Must Be Tested On The First Visit
- Identification only:
  - board identity,
  - connector identity,
  - interface type,
  - power facts,
  - ESTOP-chain understanding,
  - allowed procedure boundaries.

## What Must NOT Be Tested Yet
- Unapproved motion tests.
- Direct drive commands to motors.
- GPIO experiments on unknown lines.
- Board-specific control code deployment.
- Any test that risks bypassing the local safety contour.

## Required Evidence Artifacts
- A dated photo set.
- Structured notes for board, connectors, power, interfaces, and ESTOP chain.
- A short hardware-facts report with verified vs not verified separation.
