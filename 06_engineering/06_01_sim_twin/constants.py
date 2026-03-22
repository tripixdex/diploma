from __future__ import annotations

# Sources
SOURCE_TWIN = "twin"
SOURCE_SYSTEM = "system"
SOURCE_OPERATOR = "operator"
SOURCE_SENSOR = "sensor"

# Topics
TOPIC_CMD_MANUAL = "agv/denford/v1/cmd/manual"
TOPIC_CMD_MODE = "agv/denford/v1/cmd/mode"
TOPIC_CMD_RESET = "agv/denford/v1/cmd/reset"
TOPIC_STATE_STATUS = "agv/denford/v1/state/status"
TOPIC_STATE_TELEMETRY = "agv/denford/v1/state/telemetry"
TOPIC_EVENT_ALARM = "agv/denford/v1/event/alarm"
TOPIC_EVENT_FAULT = "agv/denford/v1/event/fault"
TOPIC_EVENT_AUDIT = "agv/denford/v1/event/audit"
TOPIC_HEALTH_HEARTBEAT = "agv/denford/v1/health/heartbeat"

# Message types
MESSAGE_TYPE_STATUS = "status"
MESSAGE_TYPE_TELEMETRY = "telemetry"
MESSAGE_TYPE_AUDIT = "audit"
MESSAGE_TYPE_ALARM = "alarm"
MESSAGE_TYPE_FAULT = "fault"
MESSAGE_TYPE_HEARTBEAT = "heartbeat"

# Severity
SEVERITY_INFO = "info"
SEVERITY_WARNING = "warning"
SEVERITY_CRITICAL = "critical"

# Audit semantics
AUDIT_RESULT_ACCEPTED = "accepted"
AUDIT_RESULT_REJECTED = "rejected"
AUDIT_REASON_ILLEGAL_TRANSITION = "illegal_transition"
AUDIT_REASON_INVALID_COMMAND = "invalid_command"
AUDIT_REASON_MANUAL_COMMAND_ACCEPTED = "manual_command_accepted"
AUDIT_REASON_MANUAL_COMMAND_OUTSIDE_MANUAL_MODE = "manual_command_outside_manual_mode"
AUDIT_REASON_MANUAL_COMMAND_BLOCKED_BY_SAFETY = "manual_command_blocked_by_safety"

# Alarm and fault reasons
REASON_ESTOP_LATCHED = "estop_latched"
REASON_LINK_DEGRADED = "link_degraded"

# Payload keys
PAYLOAD_KEY_PREV_STATE = "prev_state"
PAYLOAD_KEY_TRANSITION_REASON = "transition_reason"
PAYLOAD_KEY_TRACTION_ENABLED = "traction_enabled"
PAYLOAD_KEY_RESULT = "result"
PAYLOAD_KEY_REASON = "reason"
PAYLOAD_KEY_EVENT_TYPE = "event_type"
PAYLOAD_KEY_LINK_OK = "link_ok"
PAYLOAD_KEY_LINEAR = "linear"
PAYLOAD_KEY_ANGULAR = "angular"
PAYLOAD_KEY_LINE_SENSOR_STATE = "line_sensor_state"
PAYLOAD_KEY_DOCKING_STATE = "docking_state"

# Telemetry literals
LINE_SENSOR_STATE_DETECTED = "line_detected"
DOCKING_STATE_COMPLETE = "dock_complete"

# Scenario placeholders
INVALID_MODE_REQUEST_REASON = "mode_request_not_allowed_in_current_state"
