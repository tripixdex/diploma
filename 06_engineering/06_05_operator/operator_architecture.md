# Operator Architecture

## Purpose
- Provide a minimal operator-facing client contour for observation and command dispatch.

## Boundaries
- `operator_api_client.py`: read-only backend REST access.
- `operator_ws_client.py`: backend live update subscription.
- `operator_commands.py`: MQTT command publisher for operator actions.
- `operator_demo_runner.py`: local integration demo harness only.

## Runtime Flow
1. Operator client connects to backend REST and obtains current status, recent events, and recent telemetry.
2. Operator client opens a backend WebSocket subscription for live updates.
3. Operator command publisher sends contract-shaped MQTT commands.
4. Existing Stage 4 transport and Stage 3 edge runtime process commands.
5. Existing Stage 5 backend ingests resulting command/event/status/telemetry messages.
6. Operator client observes updated backend state and live frames.

## Why This Is Minimal
- No heavy frontend framework is introduced.
- No new protocol is invented; existing backend API and MQTT contract are reused.
- No hardware integration is added.
- Demo execution remains local and stage-scoped.
