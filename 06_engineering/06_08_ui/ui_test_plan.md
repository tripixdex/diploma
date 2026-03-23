# UI Test Plan

## Stage 7D Checks
- UI dev server starts successfully.
- UI can read current status from backend REST.
- UI can read recent events, commands, and telemetry from backend REST.
- UI can receive WebSocket live updates from backend.
- UI can dispatch `mode`, `manual`, and `reset` commands through backend REST.
- UI reflects rejected outcomes through backend audit/event evidence.

## Out Of Scope
- pixel-perfect cross-browser QA;
- production asset pipeline hardening;
- authentication/authorization;
- hardware-phase UI behavior.

## Required Validation Before Closeout
- `ui_demo_stack.py` runs.
- Vite UI starts and serves the app.
- backend REST remains functional.
- backend WebSocket remains functional.
- Stage 7 demo remains runnable.
