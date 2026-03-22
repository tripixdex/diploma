# Operator Test Plan

## Stage 6 verifies
- backend REST path can provide current status, recent events, recent commands, and recent telemetry to an operator-facing client;
- backend WebSocket path can provide live updates to an operator-facing client;
- operator client can publish contract-shaped mode, manual, and reset commands through MQTT;
- existing Stage 3 edge and Stage 4 transport path react without regression;
- operator console flow remains lightweight and local.

## Stage 6 does not verify
- final web UI usability;
- hardware integration;
- Webots integration;
- production deployment or authentication/authorization.

## Mandatory evidence before closeout
- operator demo fetches current status from backend;
- operator demo fetches recent events and telemetry from backend;
- operator demo subscribes to backend live updates;
- operator demo sends mode, manual, and reset commands;
- Stage 5 backend demo still runs;
- Stage 4 transport demo still runs;
- Stage 3 edge demo still runs;
- Stage 2 scenario runner still reports full PASS.
