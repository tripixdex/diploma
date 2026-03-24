# Minimal Regression Baseline

## What This Suite Covers
- Valid core state transition behavior in the software-only edge/domain path.
- Illegal transition rejection.
- Heartbeat-driven degradation trigger.
- Prolonged disconnect escalation to `SAFE_STOP`.
- Backend request validation for:
  - invalid mode,
  - invalid manual range,
  - illegal reset/state pairing.
- Truth-loop invariant:
  - command dispatch must not be treated as command acceptance.

## What This Suite Does Not Cover
- Full broker-backed integration.
- Full browser/UI automation.
- Broad API coverage.
- Storage durability or PostgreSQL behavior.
- Hardware, deployment, or Webots behavior.
- Performance, load, or concurrency claims.

## How To Run
- From the repo root:
  - `python3 -m unittest discover -s tests -p 'test_*.py' -v`

## How To Interpret Failures
- A failing edge/domain test means a critical software-only state or heartbeat invariant drifted.
- A failing backend validation test means the API contract is no longer rejecting obviously unsafe or unsupported input correctly.
- A failing truth-loop test means the system may be blurring the line between dispatch and acceptance, which is not allowed in the current MVP.

## Why This Is Minimal, Not Comprehensive
- The goal is to give reviewers one small, deterministic regression baseline around critical behavior.
- The suite intentionally avoids pretending that broad system coverage, full UI automation, or deployment/hardware validation already exist.
- This suite is a floor for critical software-only regressions, not a claim of overall test completeness.
