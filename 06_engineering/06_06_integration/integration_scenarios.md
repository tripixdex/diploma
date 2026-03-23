# Integration Scenarios

## Scenario Set

### 1. Startup full chain
- Preconditions: local broker path available, software-only services not started yet.
- Trigger: integration runner starts broker, edge gateway, backend bridge, and operator-facing clients.
- Expected result: edge bootstraps to `IDLE`, backend ingests retained status, operator can read initial status.

### 2. Operator gets initial status
- Preconditions: startup full chain completed.
- Trigger: operator REST client requests current status.
- Expected result: backend returns `IDLE` status shaped by the MQTT contract.

### 3. Operator sends mode command
- Preconditions: current state `IDLE`.
- Trigger: operator publishes `cmd/mode` with requested mode `MANUAL`.
- Expected result: edge accepts transition to `MANUAL`, backend stores command + audit + status evidence, operator sees live update.

### 4. Operator sends manual command
- Preconditions: current state `MANUAL`.
- Trigger: operator publishes `cmd/manual`.
- Expected result: edge accepts manual command, telemetry is published, backend stores command + telemetry evidence.

### 5. Edge emits status / telemetry / event
- Preconditions: mode/manual flow already executed.
- Trigger: edge transitions and runtime actions emit contract-shaped records.
- Expected result: backend receives status, telemetry, audit, heartbeat, and later degraded alarm evidence.

### 6. Backend stores and serves data
- Preconditions: command/event/status/telemetry traffic already produced.
- Trigger: operator queries backend REST endpoints.
- Expected result: current status, recent commands, recent events, and recent telemetry all return non-empty contract-compatible data.

### 7. Operator receives live update
- Preconditions: WebSocket subscription opened before operator actions.
- Trigger: mode/manual/degraded flow occurs.
- Expected result: operator receives live frames including handshake plus contract-shaped updates.

### 8. Heartbeat timeout -> degraded path
- Preconditions: current state `MANUAL`.
- Trigger: integration runner advances heartbeat ticks until timeout.
- Expected result: edge transitions to `DISCONNECTED_DEGRADED`, publishes audit + status + alarm + heartbeat, backend stores them, operator sees degraded evidence.

### 9. Invalid command rejection
- Preconditions: operator command path active.
- Trigger: operator publishes unsupported mode request.
- Expected result: transport maps it to invalid command, edge rejects it, backend stores audit rejection, state remains unchanged.

### 10. Reset / clear path behavior according to current contract
- Preconditions: current state `MANUAL`.
- Trigger: operator publishes `reset_action=clear_safe_stop`.
- Expected result: request travels through the path, but current contract/state rules reject it in `MANUAL`; rejection is evidenced via audit and command history without false success claims.
