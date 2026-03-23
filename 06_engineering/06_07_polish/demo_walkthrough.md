# Demo Walkthrough

## What we show
- A frozen software-only modernization contour for AGV Denford.
- End-to-end path from operator action to edge reaction and back to backend/operator visibility.
- Honest degraded behavior when heartbeat is lost.
- Honest rejection of an invalid command.

## Recommended demo order
1. Start the software-only demo runner.
2. Show that the system starts in a safe visible state.
3. Show that the operator can read current status.
4. Show a valid mode change to `MANUAL`.
5. Show a valid manual command.
6. Show that MQTT transfer occurred and the edge side reacted.
7. Show that backend persistence and operator live updates are visible.
8. Show heartbeat loss and transition to `DISCONNECTED_DEGRADED`.
9. Show rejection of an invalid command.
10. End with the final summary and freeze statement.

## What the supervisor will see
- Console evidence of startup.
- Console evidence of command flow.
- Console evidence of state/event/telemetry propagation.
- Console evidence of backend visibility.
- Console evidence of degraded behavior and invalid command rejection.
- A final statement that the MVP is software-only and frozen before hardware work.

## What this proves
- The project is no longer only a plan or a contract set.
- The software contour works end-to-end in a repeatable way.
- Safety-relevant degraded behavior is modeled explicitly.
- Backend and operator paths are integrated, not isolated demos.

## What this does not prove
- Real Raspberry Pi behavior.
- Real Denford wiring compatibility.
- Real motor/sensor integration.
- Lab-phase electrical or mechanical readiness.
