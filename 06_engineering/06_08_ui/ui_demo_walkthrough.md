# UI Demo Walkthrough

## What To Show
1. Open the UI and confirm the system card loads current state.
2. Point at recent events and recent commands to show backend history.
3. Show telemetry snapshot and live updates panel.
4. Send a `MANUAL` mode command.
5. Send a small manual motion command.
6. Show audit/status/telemetry updates appearing in the live feed and history panels.
7. Trigger a reset path action and show honest rejection if the contract blocks it.
8. Let heartbeat loss drive the system to degraded behavior and show the alert clearly.

## What The Supervisor Sees
- one calm screen instead of scattered console output;
- clear separation between status, control, history, telemetry, and live updates;
- evidence that the software-only chain is connected end to end.

## What This Proves
- backend REST + WebSocket are usable by a human-facing client;
- operator commands traverse the frozen MVP path;
- rejected or degraded outcomes are visible and not hidden.

## What This Does Not Prove
- real Raspberry Pi binding;
- real AGV wiring;
- GPIO access;
- hardware-phase performance.
