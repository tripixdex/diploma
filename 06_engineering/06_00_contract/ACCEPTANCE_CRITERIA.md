# Acceptance Criteria

## Stage 1 Contract Completeness Criteria
- System boundary, actors, subsystems, and safety principles are explicitly defined.
- State machine covers all approved minimum states and transition rules.
- Logical I/O is separated from hardware-dependent mapping.
- MQTT topic namespace, roles, QoS, retained policy, and JSON schema are frozen at contract level.
- Command acknowledgement, timeout, and illegal transition behavior are explicitly defined.
- Minimum validation scenarios are documented with expected state and MQTT evidence.
- Open questions are isolated from the frozen contract and do not silently leak into assumptions.

## Future Validation-Oriented Criteria for Stage 2+
- Stage 2 must demonstrate that the simulation scaffold can exercise the documented modes and transitions.
- Stage 3 must show edge runtime behavior traceable to the Stage 1 state machine and I/O contract.
- Stage 4 must show MQTT traffic matching the topic and payload contract.
- Stage 5 must show backend ingestion/storage consuming the documented state, telemetry, and event streams.
- Stage 6 must show operator actions mapping only to allowed contract commands.
- Stage 7 must provide scenario evidence aligned to the expectations below.

## Minimum Scenario List

### Startup
- Preconditions: controller process starts, no active e-stop, minimum startup checks pass.
- Trigger: startup sequence begins.
- Expected state transition: `INIT -> IDLE`.
- Expected MQTT evidence: `event/audit` startup event, then `state/status` showing `IDLE`, heartbeat publication begins.
- Expected safety behavior: traction remains disabled until `IDLE` is reached and a valid motion-capable mode is later accepted.

### Manual Mode
- Preconditions: current state `IDLE`, no active e-stop, no active obstacle, link healthy.
- Trigger: valid `cmd/mode` request for `MANUAL`, followed by valid `cmd/manual`.
- Expected state transition: `IDLE -> MANUAL`.
- Expected MQTT evidence: `event/audit` acceptance for mode command, `state/status` for `MANUAL`, telemetry and heartbeat updates, audit for manual command handling.
- Expected safety behavior: bounded motion only while safety inputs remain valid; invalid or stale commands do not persist motion authority.

### Auto Line Mode
- Preconditions: current state `IDLE`, line sensor health valid, no active e-stop, no blocking obstacle.
- Trigger: valid `cmd/mode` request for `AUTO_LINE`.
- Expected state transition: `IDLE -> AUTO_LINE`.
- Expected MQTT evidence: `event/audit` acceptance, `state/status` for `AUTO_LINE`, `state/telemetry` including line sensor snapshot.
- Expected safety behavior: local line-following remains bounded; loss of line or obstacle input must remove motion authority.

### E-Stop
- Preconditions: any non-fault state, system may be stationary or moving.
- Trigger: `estop_active` becomes true.
- Expected state transition: `* -> ESTOP_LATCHED`.
- Expected MQTT evidence: immediate `event/alarm`, `event/fault`, and `state/status` with `ESTOP_LATCHED`; heartbeat reflects latched state.
- Expected safety behavior: traction disabled immediately, no command can restore motion until valid reset path is completed.

### Obstacle
- Preconditions: current state `MANUAL` or `AUTO_LINE`.
- Trigger: `obstacle_detected` becomes true.
- Expected state transition: `MANUAL -> SAFE_STOP` or `AUTO_LINE -> SAFE_STOP`.
- Expected MQTT evidence: `event/alarm` with obstacle reason, `state/status` with `SAFE_STOP`, telemetry snapshot reflecting obstacle input.
- Expected safety behavior: motion authority removed; resumption requires explicit clear and accepted recovery path.

### Loss Link
- Preconditions: current state `MANUAL` or `AUTO_LINE`, broker/backend heartbeat is healthy.
- Trigger: heartbeat timeout exceeds contract threshold.
- Expected state transition: `MANUAL -> DISCONNECTED_DEGRADED` or `AUTO_LINE -> DISCONNECTED_DEGRADED`.
- Expected MQTT evidence: last successful heartbeat, local audit/alarm buffering or later publication when link returns, `state/status` update if transport is still partially available.
- Expected safety behavior: controller degrades to non-authoritative communications mode and removes or restricts motion authority; if uncertainty persists, `SAFE_STOP` follows.

### Docking
- Preconditions: current state `AUTO_LINE` or docking-capable bounded flow, docking sensors available logically.
- Trigger: docking completion condition becomes true.
- Expected state transition: `AUTO_LINE -> IDLE` or docking sub-flow complete within `AUTO_LINE` followed by `IDLE`.
- Expected MQTT evidence: `state/telemetry` with docking sensor snapshot, `event/audit` for docking completion, `state/status` returning to `IDLE`.
- Expected safety behavior: docking completion must end with motion neutralized unless a new valid command is accepted.

### Invalid Command Rejection
- Preconditions: controller in any state where requested action is forbidden.
- Trigger: illegal `cmd/mode`, illegal `cmd/reset`, or out-of-context `cmd/manual`.
- Expected state transition: no state change.
- Expected MQTT evidence: `event/audit` with `result=rejected`, rejection reason, original `corr_id`; `event/fault` only if unsafe inconsistency is detected.
- Expected safety behavior: controller remains in current safe state and never enables motion from a rejected command.

## Stage 1 Closeout Test
Stage 1 is acceptable for closeout if every scenario above has an unambiguous expected transition, MQTT evidence path, and safety behavior, even though runtime validation itself belongs to later stages.
