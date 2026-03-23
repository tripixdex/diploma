# State Machine

## Scope Note
This file now describes the state machine that is actually implemented and evidenced in the current software-only MVP. `MAINTENANCE` and its transitions are explicitly deferred and are not part of the active pre-hardware gate.

## Implemented States
- `INIT`
- `IDLE`
- `MANUAL`
- `AUTO_LINE`
- `SAFE_STOP`
- `ESTOP_LATCHED`
- `FAULT`
- `DISCONNECTED_DEGRADED`

Deferred beyond the current MVP:
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
| `DISCONNECTED_DEGRADED` | Communications degraded; motion authority removed while the system waits for link restore or safe-stop escalation. |

## Allowed Transitions In Current MVP
| From | To | Trigger Event | Notes |
| --- | --- | --- | --- |
| `INIT` | `IDLE` | `startup_ok` | Minimum checks passed. |
| `INIT` | `FAULT` | `startup_fault` | Mandatory initialization failure. |
| `IDLE` | `MANUAL` | `mode_manual_requested` | Command accepted and safety preconditions hold. |
| `IDLE` | `AUTO_LINE` | `mode_auto_line_requested` | Command accepted and line-following preconditions hold. |
| `IDLE` | `SAFE_STOP` | `protective_stop_request` | Preventive safe halt. |
| `IDLE` | `ESTOP_LATCHED` | `estop_triggered` | Highest-priority transition. |
| `IDLE` | `FAULT` | `fault_detected` | Local fault. |
| `MANUAL` | `IDLE` | `manual_stop_requested` | Motion cancelled cleanly. |
| `MANUAL` | `SAFE_STOP` | `obstacle_detected` or `safe_stop_requested` | Protective stop. |
| `MANUAL` | `ESTOP_LATCHED` | `estop_triggered` | Immediate latching. |
| `MANUAL` | `FAULT` | `fault_detected` | Fault path. |
| `MANUAL` | `DISCONNECTED_DEGRADED` | `heartbeat_lost` | Initial connectivity degradation. |
| `AUTO_LINE` | `IDLE` | `auto_line_complete` or `mode_idle_requested` | Controlled exit. |
| `AUTO_LINE` | `SAFE_STOP` | `obstacle_detected`, `line_lost`, or `safe_stop_requested` | Motion stopped. |
| `AUTO_LINE` | `ESTOP_LATCHED` | `estop_triggered` | Immediate latching. |
| `AUTO_LINE` | `FAULT` | `fault_detected` | Fault path. |
| `AUTO_LINE` | `DISCONNECTED_DEGRADED` | `heartbeat_lost` | Initial connectivity degradation. |
| `SAFE_STOP` | `IDLE` | `safe_stop_cleared` | Preconditions safe and operator/system reset accepted. |
| `SAFE_STOP` | `ESTOP_LATCHED` | `estop_triggered` | Escalation. |
| `SAFE_STOP` | `FAULT` | `fault_detected` | Escalation. |
| `ESTOP_LATCHED` | `IDLE` | `estop_reset_accepted` | Only after local reset conditions and command acceptance. |
| `DISCONNECTED_DEGRADED` | `IDLE` | `link_restored_and_safe` | Communications restored and no active stop/fault. |
| `DISCONNECTED_DEGRADED` | `SAFE_STOP` | `prolonged_disconnect` | Link loss persisted beyond the degraded grace window. |
| `DISCONNECTED_DEGRADED` | `SAFE_STOP` | `protective_stop_request` | Safe-stop demand while already degraded. |
| `DISCONNECTED_DEGRADED` | `FAULT` | `fault_detected` | Escalation. |
| `DISCONNECTED_DEGRADED` | `ESTOP_LATCHED` | `estop_triggered` | Highest-priority path. |
| `FAULT` | `IDLE` | `fault_reset_accepted` | Only after diagnostics and safe conditions. |

## Forbidden Transitions
- Any direct transition into `MANUAL` or `AUTO_LINE` from `INIT`.
- Any direct transition from `ESTOP_LATCHED` to `MANUAL` or `AUTO_LINE`.
- Any direct transition from `FAULT` to `MANUAL` or `AUTO_LINE`.
- Any direct transition from `DISCONNECTED_DEGRADED` to `MANUAL` or `AUTO_LINE`.
- Any transition that enables motion while `estop_active`, `obstacle_active`, or mandatory link validity is false.
- Any cloud-only command that attempts to override local safety latching.

## Trigger Events In Current MVP
- `startup_ok`
- `startup_fault`
- `mode_manual_requested`
- `mode_auto_line_requested`
- `mode_idle_requested`
- `manual_stop_requested`
- `safe_stop_requested`
- `protective_stop_request`
- `safe_stop_cleared`
- `obstacle_detected`
- `estop_triggered`
- `estop_reset_accepted`
- `fault_detected`
- `fault_reset_accepted`
- `heartbeat_lost`
- `prolonged_disconnect`
- `link_restored_and_safe`
- `auto_line_complete`
- `manual_command`
- `invalid_command`

Deferred trigger set beyond current MVP:
- `mode_maintenance_requested`
- `maintenance_requested`
- `maintenance_exit_requested`
- `reset_failed`

## Entry Actions
| State | Entry Actions |
| --- | --- |
| `INIT` | Disable traction, initialize runtime context, publish initial status. |
| `IDLE` | Disable motion command output, publish steady state status. |
| `MANUAL` | Enable bounded manual control path, publish mode transition audit. |
| `AUTO_LINE` | Enable bounded line-following logic, publish mode transition audit. |
| `SAFE_STOP` | Disable traction or issue stop command, raise alarm/event, preserve last reason. |
| `ESTOP_LATCHED` | Disable traction, latch emergency reason, publish alarm/fault immediately. |
| `FAULT` | Disable traction, capture fault code/context, publish fault event. |
| `DISCONNECTED_DEGRADED` | Remove motion authority, mark communications degraded, publish alarm plus heartbeat degradation evidence. |

## MQTT Publication On Key Transitions
| Transition Type | MQTT Publications |
| --- | --- |
| Any accepted state transition | `agv/denford/v1/state/status` with old/new state and mode. |
| Transition caused by operator command | `agv/denford/v1/event/audit` with `corr_id`, command outcome, and actor source. |
| Transition to `SAFE_STOP` | `agv/denford/v1/event/alarm` and `agv/denford/v1/state/status`. |
| Transition to `ESTOP_LATCHED` | `agv/denford/v1/event/alarm`, `agv/denford/v1/event/fault`, and `agv/denford/v1/state/status`. |
| Transition to `FAULT` | `agv/denford/v1/event/fault` and `agv/denford/v1/state/status`. |
| Transition to `DISCONNECTED_DEGRADED` | `agv/denford/v1/event/alarm`, heartbeat with `link_ok=false`, and latest `state/status`. |
| Prolonged disconnect escalation | `agv/denford/v1/event/alarm` with `reason=prolonged_disconnect`, `state/status` for `SAFE_STOP`, and heartbeat with `link_ok=false`. |
| Rejected transition | `agv/denford/v1/event/audit` with rejection reason and `agv/denford/v1/event/fault` only if the rejection indicates a fault condition. |
