# Minimal Regression Tests

This directory contains the minimal automated regression baseline for the current software-only MVP.

## What Is Covered
- Critical edge/domain behavior:
  - valid core transition,
  - illegal transition rejection,
  - heartbeat degradation,
  - prolonged disconnect escalation to `SAFE_STOP`.
- Critical backend validation behavior:
  - invalid mode rejection,
  - invalid manual range rejection,
  - illegal reset/state pairing rejection.
- Critical truth-loop invariant:
  - dispatch is not the same thing as acceptance.

## What Is Not Covered
- Full browser/UI automation.
- Full broker-backed end-to-end integration.
- Broad storage/API coverage.
- Hardware, deployment, or Webots behavior.

## Why This Exists
- To give reviewers one small, deterministic regression layer around critical software-only behavior.
- To avoid pretending comprehensive test coverage exists when it does not.

## How To Run
- `python3 -m unittest discover -s tests -p 'test_*.py' -v`
