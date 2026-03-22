# Scenario Model

## Startup
- Input conditions: runtime created in `INIT`, no active e-stop, no startup fault.
- Trigger: `startup_ok`.
- Expected transition: `INIT -> IDLE`.
- What must be published: startup audit, status showing `IDLE`, heartbeat.
- Success criteria: runtime reaches `IDLE` and stores a visible status/audit trace.

## Manual Mode
- Input conditions: current state `IDLE`, no obstacle, no e-stop, link healthy.
- Trigger: `mode_manual_requested`.
- Expected transition: `IDLE -> MANUAL`.
- What must be published: audit accept, status for `MANUAL`, optional telemetry/heartbeat.
- Success criteria: state becomes `MANUAL` and a subsequent manual command can be accepted without violating safety flags.

## Auto Line Mode
- Input conditions: current state `IDLE`, line-following preconditions valid, no blocking safety input.
- Trigger: `mode_auto_line_requested`.
- Expected transition: `IDLE -> AUTO_LINE`.
- What must be published: audit accept, status for `AUTO_LINE`, telemetry with line context.
- Success criteria: state becomes `AUTO_LINE` and line-related events can affect behavior.

## Obstacle
- Input conditions: current state `MANUAL` or `AUTO_LINE`.
- Trigger: `obstacle_detected`.
- Expected transition: `MANUAL -> SAFE_STOP` or `AUTO_LINE -> SAFE_STOP`.
- What must be published: alarm plus status for `SAFE_STOP`.
- Success criteria: state becomes `SAFE_STOP`, traction-equivalent motion authority is removed logically.

## E-Stop
- Input conditions: any runtime state.
- Trigger: `estop_triggered`.
- Expected transition: `* -> ESTOP_LATCHED`.
- What must be published: alarm, fault, status with `ESTOP_LATCHED`.
- Success criteria: state latches into `ESTOP_LATCHED` and motion-capable transitions are blocked until reset path is valid.

## Loss Link
- Input conditions: current state `MANUAL` or `AUTO_LINE`, link previously healthy.
- Trigger: `heartbeat_lost`.
- Expected transition: `MANUAL -> DISCONNECTED_DEGRADED` or `AUTO_LINE -> DISCONNECTED_DEGRADED`.
- What must be published: degraded alarm, status, heartbeat evidence where possible.
- Success criteria: runtime enters degraded state and does not continue as normal motion authority.

## Docking
- Input conditions: current state `AUTO_LINE`, docking path active logically.
- Trigger: `auto_line_complete`.
- Expected transition: `AUTO_LINE -> IDLE`.
- What must be published: audit for docking completion, status returning to `IDLE`, telemetry snapshot.
- Success criteria: docking completion ends in safe non-motion state.

## Invalid Command Rejection
- Input conditions: runtime state where requested transition is forbidden.
- Trigger: invalid mode request, invalid manual command, or invalid reset.
- Expected transition: no transition.
- What must be published: audit rejection and fault only if the situation indicates internal inconsistency.
- Success criteria: authoritative state remains unchanged and rejection is visible in the fake publication log.
