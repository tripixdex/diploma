# Stage 2 Scenario Evidence

## Execution Baseline
- Command used: `python3 06_engineering/06_01_sim_twin/run_stage2_scenarios.py`
- Runtime type: local in-memory twin runtime
- Transport type: no real MQTT, only in-memory publisher
- Result summary: `8 / 8 PASS`

## Startup
- Preconditions: runtime created in `INIT`, no active e-stop, no startup fault.
- Trigger: `startup_ok`
- Expected transition: `INIT -> IDLE`
- Actual transition: `INIT -> IDLE`
- Expected published evidence: `event/audit`, `state/status`, `health/heartbeat`
- Actual published evidence: `event/audit`, `state/status`, `health/heartbeat`
- Pass/Fail: PASS
- Notes: final state `IDLE`

## Manual Mode
- Preconditions: runtime in `IDLE` after startup, no obstacle, no e-stop, link healthy.
- Trigger: `mode_manual_requested` plus `manual_command`
- Expected transition: `IDLE -> MANUAL`, then manual command accepted in `MANUAL`
- Actual transition: `INIT -> IDLE | IDLE -> MANUAL | MANUAL -> MANUAL`
- Expected published evidence: `event/audit`, `state/status`, `state/telemetry`, `health/heartbeat`
- Actual published evidence: `event/audit`, `state/status`, `state/telemetry`, `health/heartbeat`
- Pass/Fail: PASS
- Notes: manual command is accepted without changing authoritative state away from `MANUAL`

## Auto Line Mode
- Preconditions: runtime in `IDLE` after startup, line-following preconditions valid, no blocking safety input.
- Trigger: `mode_auto_line_requested`
- Expected transition: `IDLE -> AUTO_LINE`
- Actual transition: `INIT -> IDLE | IDLE -> AUTO_LINE`
- Expected published evidence: `event/audit`, `state/status`, `state/telemetry`, `health/heartbeat`
- Actual published evidence: `event/audit`, `state/status`, `state/telemetry`, `health/heartbeat`
- Pass/Fail: PASS
- Notes: telemetry contains a logical line sensor snapshot, not hardware data

## Obstacle
- Preconditions: runtime in `MANUAL`
- Trigger: `obstacle_detected`
- Expected transition: `MANUAL -> SAFE_STOP`
- Actual transition: `INIT -> IDLE | IDLE -> MANUAL | MANUAL -> SAFE_STOP`
- Expected published evidence: `event/audit`, `state/status`, `event/alarm`, `health/heartbeat`
- Actual published evidence: `event/audit`, `state/status`, `event/alarm`, `health/heartbeat`
- Pass/Fail: PASS
- Notes: final state `SAFE_STOP`

## E-Stop
- Preconditions: runtime in `MANUAL`, reset path available after latch
- Trigger: `estop_triggered` plus `estop_reset_accepted`
- Expected transition: `MANUAL -> ESTOP_LATCHED -> IDLE`
- Actual transition: `INIT -> IDLE | IDLE -> MANUAL | MANUAL -> ESTOP_LATCHED | ESTOP_LATCHED -> IDLE`
- Expected published evidence: `event/audit`, `state/status`, `event/alarm`, `event/fault`, `health/heartbeat`
- Actual published evidence: `event/audit`, `state/status`, `event/alarm`, `event/fault`, `health/heartbeat`
- Pass/Fail: PASS
- Notes: e-stop latch is visible before reset back to `IDLE`

## Loss Link
- Preconditions: runtime in `MANUAL`, link initially healthy
- Trigger: `heartbeat_lost` plus `link_restored_and_safe`
- Expected transition: `MANUAL -> DISCONNECTED_DEGRADED -> IDLE`
- Actual transition: `INIT -> IDLE | IDLE -> MANUAL | MANUAL -> DISCONNECTED_DEGRADED | DISCONNECTED_DEGRADED -> IDLE`
- Expected published evidence: `event/audit`, `state/status`, `event/alarm`, `health/heartbeat`
- Actual published evidence: `event/audit`, `state/status`, `event/alarm`, `health/heartbeat`
- Pass/Fail: PASS
- Notes: degraded heartbeat shows `link_ok=false` during degraded state

## Docking
- Preconditions: runtime in `AUTO_LINE` with logical docking completion event available
- Trigger: `auto_line_complete`
- Expected transition: `AUTO_LINE -> IDLE`
- Actual transition: `INIT -> IDLE | IDLE -> AUTO_LINE | AUTO_LINE -> IDLE`
- Expected published evidence: `event/audit`, `state/status`, `state/telemetry`, `health/heartbeat`
- Actual published evidence: `event/audit`, `state/status`, `state/telemetry`, `health/heartbeat`
- Pass/Fail: PASS
- Notes: telemetry contains logical docking completion evidence

## Invalid Command Rejection
- Preconditions: runtime in `IDLE`, invalid operator command injected
- Trigger: `invalid_command`
- Expected transition: no state change, remain in `IDLE`
- Actual transition: `INIT -> IDLE | IDLE -> IDLE`
- Expected published evidence: `event/audit` rejection
- Actual published evidence: `event/audit` rejection
- Pass/Fail: PASS
- Notes: no state mutation occurs on rejected command
