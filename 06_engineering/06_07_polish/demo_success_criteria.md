# Demo Success Criteria

The Stage 7B demo is successful only if all of the following are true:

1. The demo runner starts the software-only chain without manual code edits.
2. Initial status is visible and reflects a valid startup state.
3. Operator mode command is accepted and reflected in downstream evidence.
4. Operator manual command is accepted and reflected in downstream evidence.
5. Edge reaction is visible through MQTT-backed transport.
6. Backend stores and serves command/event/status/telemetry evidence.
7. Operator live feed receives updates during the run.
8. Heartbeat loss drives the contour into `DISCONNECTED_DEGRADED`.
9. Invalid command rejection is explicit and visible.
10. Final summary stays honest about software-only scope and deferred hardware work.

The demo is not successful if any of the following occur:
- the chain runs only partially;
- operator evidence is missing;
- degraded behavior does not appear;
- invalid command rejection is not visible;
- the demo implies hardware readiness that was not validated.
