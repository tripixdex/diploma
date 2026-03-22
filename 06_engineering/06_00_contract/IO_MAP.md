# IO Map

## Purpose
This document defines the logical I/O contract for V1. It freezes signal intent without claiming exact electrical mapping before the hardware survey is completed.

## Logical Input Groups

### Line Sensors
- `line_left_detect`
- `line_center_detect`
- `line_right_detect`
- `line_sensor_health`
- Purpose: support bounded `AUTO_LINE` logic and loss-of-line detection.

### Docking Sensors
- `dock_present`
- `dock_alignment_ok`
- `dock_contact_or_position_reached`
- Purpose: bounded docking completion or approach evidence.

### Obstacle Sensor
- `obstacle_detected`
- `obstacle_sensor_health`
- Purpose: trigger protective stop and alarm publication.

### E-Stop Input
- `estop_active`
- `estop_reset_permitted`
- Purpose: preserve local safety contour and latch emergency-stop behavior.

### Heartbeat / Link Status
- `broker_link_ok`
- `backend_link_ok`
- `heartbeat_age_ms`
- Purpose: detect communication degradation and drive `DISCONNECTED_DEGRADED`.

### Operator Commands
- `requested_mode`
- `manual_motion_vector`
- `reset_request`
- `ack_request`
- Purpose: accept bounded operator intent through validated command channels.

## Logical Output Groups

### Traction Enable / Disable
- `traction_enable`
- `traction_disable`
- `brake_or_stop_request`
- Purpose: explicit motion authority control, always safety-gated.

### Motion Command Group
- `motion_linear_cmd`
- `motion_angular_cmd`
- `line_follow_enable`
- `dock_approach_enable`
- Purpose: bounded motion requests in `MANUAL` or `AUTO_LINE`.

### Status Publish
- `current_state`
- `current_mode`
- `connectivity_status`
- `hardware_status_summary`
- Purpose: authoritative edge state publication.

### Event / Alarm Publish
- `alarm_code`
- `fault_code`
- `audit_event`
- `transition_reason`
- Purpose: external visibility of safety and control-relevant events.

### Telemetry Publish
- `position_or_progress_estimate`
- `speed_estimate`
- `sensor_snapshot`
- `heartbeat_metrics`
- `runtime_health_metrics`
- Purpose: periodic evidence and operator/backend visibility.

## Logical Signals
| Signal | Direction | Meaning |
| --- | --- | --- |
| `estop_active` | Input | Local emergency-stop status; highest-priority inhibit. |
| `obstacle_detected` | Input | Protective stop trigger. |
| `line_*` | Input | Logical line-following sensor set. |
| `dock_*` | Input | Docking-related logical sensor set. |
| `requested_mode` | Input | Requested target mode from operator command path. |
| `manual_motion_vector` | Input | Bounded manual motion request. |
| `traction_enable` | Output | Explicit permission for motion path. |
| `motion_*` | Output | Logical motion requests to actuator layer. |
| `current_state` | Output | Published authoritative controller state. |
| `alarm_code` | Output | Published alarm classification. |
| `sensor_snapshot` | Output | Published telemetry snapshot. |

## Hardware-Dependent Mapping
The following details are unknown and deferred until hardware survey:
- GPIO pin numbers and pull-up/pull-down requirements;
- motor driver protocol and electrical levels;
- sensor bus type, polarity, debounce, and sampling timing;
- whether obstacle and docking sensors are digital, analog, or controller-mediated;
- exact emergency-stop wiring and reset conditions;
- whether traction disable is direct GPIO, relay, motor driver command, or mixed path.

No Stage 1 claim may present these details as verified.

## What Must Go Through `HardwareAdapter`
- reading line, docking, obstacle, and e-stop signals;
- exposing normalized link and hardware health to the state machine;
- enabling/disabling traction authority;
- emitting bounded motion commands to the actuator interface;
- reading board-specific timing, debounce, and startup conditions;
- handling board-specific libraries, device names, and fallback behavior;
- converting raw hardware states into logical signal groups defined in this document.

## Contract Rule
Stage 2+ implementation may only bind logic to the logical signals above. Hardware-specific mapping remains a deferred appendix until lab survey or real AGV interface confirmation exists.
