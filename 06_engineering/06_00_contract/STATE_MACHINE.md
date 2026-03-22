# State Machine

## States
- `INIT`
- `IDLE`
- `MANUAL`
- `AUTO_LINE`
- `SAFE_STOP`
- `ESTOP_LATCHED`
- `FAULT`
- `DISCONNECTED_DEGRADED`
- `MAINTENANCE`

## State Intent
| State | Intent |
| --- | --- |
| `INIT` | Start process, validate minimum prerequisites, publish initial status. |
| `IDLE` | No motion, ready to accept valid mode commands. |
| `MANUAL` | Supervised bounded operator motion control. |
| `AUTO_LINE` | Bounded line-following operation under local safety gating. |
| `SAFE_STOP` | Controlled or immediate stop state with traction disabled. |
| `ESTOP_LATCHED` | Emergency stop active; reset is blocked until local conditions are safe. |
| `FAULT` | Internal error or unsafe condition requiring explicit recovery path. |
| `DISCONNECTED_DEGRADED` | Communications degraded; motion authority removed or reduced to safe behavior. |
| `MAINTENANCE` | Inspection/diagnostic mode with production motion path restricted. |

## Allowed Transitions
| From | To | Trigger Event | Notes |
| --- | --- | --- | --- |
| `INIT` | `IDLE` | `startup_ok` | Minimum checks passed. |
| `INIT` | `FAULT` | `startup_fault` | Mandatory initialization failure. |
| `INIT` | `ESTOP_LATCHED` | `estop_active_on_boot` | E-stop detected during startup. |
| `IDLE` | `MANUAL` | `mode_manual_requested` | Command accepted and safety preconditions hold. |
| `IDLE` | `AUTO_LINE` | `mode_auto_line_requested` | Command accepted and line-following preconditions hold. |
| `IDLE` | `MAINTENANCE` | `mode_maintenance_requested` | Maintenance entry accepted. |
| `IDLE` | `SAFE_STOP` | `protective_stop_request` | Preventive safe halt. |
| `IDLE` | `ESTOP_LATCHED` | `estop_triggered` | Highest-priority transition. |
| `IDLE` | `FAULT` | `fault_detected` | Local fault. |
| `MANUAL` | `IDLE` | `manual_stop_requested` | Motion cancelled cleanly. |
| `MANUAL` | `SAFE_STOP` | `obstacle_detected` or `safe_stop_requested` | Protective stop. |
| `MANUAL` | `ESTOP_LATCHED` | `estop_triggered` | Immediate latching. |
| `MANUAL` | `FAULT` | `fault_detected` | Fault path. |
| `MANUAL` | `DISCONNECTED_DEGRADED` | `heartbeat_lost` | Connectivity degraded. |
| `AUTO_LINE` | `IDLE` | `auto_line_complete` or `mode_idle_requested` | Controlled exit. |
| `AUTO_LINE` | `SAFE_STOP` | `obstacle_detected`, `line_lost`, or `safe_stop_requested` | Motion stopped. |
| `AUTO_LINE` | `ESTOP_LATCHED` | `estop_triggered` | Immediate latching. |
| `AUTO_LINE` | `FAULT` | `fault_detected` | Fault path. |
| `AUTO_LINE` | `DISCONNECTED_DEGRADED` | `heartbeat_lost` | Connectivity degraded. |
| `SAFE_STOP` | `IDLE` | `safe_stop_cleared` | Preconditions safe and operator/system reset accepted. |
| `SAFE_STOP` | `ESTOP_LATCHED` | `estop_triggered` | Escalation. |
| `SAFE_STOP` | `FAULT` | `fault_detected` | Escalation. |
| `ESTOP_LATCHED` | `IDLE` | `estop_reset_accepted` | Only after local reset conditions and command acceptance. |
| `ESTOP_LATCHED` | `FAULT` | `reset_failed` | Reset attempt invalid or fault detected. |
| `FAULT` | `IDLE` | `fault_reset_accepted` | Only after diagnostics and safe conditions. |
| `FAULT` | `MAINTENANCE` | `maintenance_requested` | For diagnosis without motion. |
| `DISCONNECTED_DEGRADED` | `IDLE` | `link_restored_and_safe` | Communications restored and no active stop/fault. |
| `DISCONNECTED_DEGRADED` | `SAFE_STOP` | `protective_stop_request` | Remains safe if uncertainty persists. |
| `DISCONNECTED_DEGRADED` | `FAULT` | `fault_detected` | Escalation. |
| `DISCONNECTED_DEGRADED` | `ESTOP_LATCHED` | `estop_triggered` | Highest-priority path. |
| `MAINTENANCE` | `IDLE` | `maintenance_exit_requested` | Exit diagnostics mode. |
| `MAINTENANCE` | `FAULT` | `fault_detected` | Fault path. |
| `MAINTENANCE` | `ESTOP_LATCHED` | `estop_triggered` | Highest-priority path. |

## Forbidden Transitions
- Any direct transition into `MANUAL` or `AUTO_LINE` from `INIT`.
- Any direct transition from `ESTOP_LATCHED` to `MANUAL`, `AUTO_LINE`, or `MAINTENANCE`.
- Any direct transition from `FAULT` to `MANUAL` or `AUTO_LINE`.
- Any direct transition from `DISCONNECTED_DEGRADED` to `MANUAL` or `AUTO_LINE`.
- Any transition that enables motion while `estop_active`, `obstacle_active`, or mandatory sensor validity is false.
- Any cloud-only command that attempts to override local safety latching.

## Trigger Events
- `startup_ok`
- `startup_fault`
- `estop_active_on_boot`
- `mode_manual_requested`
- `mode_auto_line_requested`
- `mode_maintenance_requested`
- `mode_idle_requested`
- `manual_stop_requested`
- `safe_stop_requested`
- `protective_stop_request`
- `obstacle_detected`
- `line_lost`
- `auto_line_complete`
- `fault_detected`
- `heartbeat_lost`
- `link_restored_and_safe`
- `estop_triggered`
- `estop_reset_accepted`
- `fault_reset_accepted`
- `maintenance_requested`
- `maintenance_exit_requested`
- `reset_failed`
- `safe_stop_cleared`

## Entry Actions
| State | Entry Actions |
| --- | --- |
| `INIT` | Disable traction, initialize runtime context, publish startup audit event. |
| `IDLE` | Disable motion command output, publish steady state status. |
| `MANUAL` | Enable bounded manual control path, publish mode transition audit. |
| `AUTO_LINE` | Enable bounded line-following logic, publish mode transition audit. |
| `SAFE_STOP` | Disable traction or issue stop command, raise alarm/event, preserve last reason. |
| `ESTOP_LATCHED` | Disable traction, latch emergency reason, publish alarm/fault immediately. |
| `FAULT` | Disable traction, capture fault code/context, publish fault event. |
| `DISCONNECTED_DEGRADED` | Remove motion authority, mark communications degraded, publish alarm when possible. |
| `MAINTENANCE` | Restrict motion, enable diagnostics context, publish maintenance audit event. |

## Exit Actions
| State | Exit Actions |
| --- | --- |
| `INIT` | Clear transient startup flags. |
| `IDLE` | Record requested next mode. |
| `MANUAL` | Clear manual command latch, issue neutral motion command. |
| `AUTO_LINE` | Clear line-following command state, issue neutral motion command. |
| `SAFE_STOP` | Require explicit clear condition before releasing stop. |
| `ESTOP_LATCHED` | Verify reset preconditions before unlatching. |
| `FAULT` | Require explicit reset reason and diagnostics acknowledgment. |
| `DISCONNECTED_DEGRADED` | Require heartbeat restoration confirmation. |
| `MAINTENANCE` | Clear diagnostic-only flags before normal operation. |

## MQTT Publication on Key Transitions
| Transition Type | MQTT Publications |
| --- | --- |
| Any accepted state transition | `agv/denford/v1/state/status` with old/new state and mode. |
| Transition caused by operator command | `agv/denford/v1/event/audit` with `corr_id`, command outcome, and actor source. |
| Transition to `SAFE_STOP` | `agv/denford/v1/event/alarm` and `agv/denford/v1/state/status`. |
| Transition to `ESTOP_LATCHED` | `agv/denford/v1/event/alarm`, `agv/denford/v1/event/fault`, and `agv/denford/v1/state/status`. |
| Transition to `FAULT` | `agv/denford/v1/event/fault` and `agv/denford/v1/state/status`. |
| Transition to `DISCONNECTED_DEGRADED` | `agv/denford/v1/event/alarm`, local heartbeat degradation evidence, and latest `state/status` when link permits. |
| Rejected transition | `agv/denford/v1/event/audit` with rejection reason and `agv/denford/v1/event/fault` only if the rejection indicates a fault condition. |
