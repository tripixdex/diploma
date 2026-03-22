# MQTT Contract

## Namespace
All V1 topics use the namespace:

`agv/denford/v1/`

This namespace is contract-level and is independent from broker host, deployment topology, or containerization details.

## Topic List
| Topic | Direction | Publisher | Subscriber | Purpose |
| --- | --- | --- | --- | --- |
| `agv/denford/v1/cmd/manual` | inbound to edge | Operator/backend control path | Edge control service | Bounded manual motion command. |
| `agv/denford/v1/cmd/mode` | inbound to edge | Operator/backend control path | Edge control service | Requested mode transition. |
| `agv/denford/v1/cmd/reset` | inbound to edge | Operator/backend control path | Edge control service | Reset/ack requests for safe-stop, fault, or e-stop recovery path. |
| `agv/denford/v1/state/status` | outbound from edge | Edge control service | Backend/operator consumers | Authoritative state and mode publication. |
| `agv/denford/v1/state/telemetry` | outbound from edge | Edge control service | Backend/operator consumers | Periodic telemetry snapshot. |
| `agv/denford/v1/event/alarm` | outbound from edge | Edge control service | Backend/operator consumers | Alarm and protective-stop events. |
| `agv/denford/v1/event/fault` | outbound from edge | Edge control service | Backend/operator consumers | Fault events and serious errors. |
| `agv/denford/v1/event/audit` | bidirectional evidence path | Edge control service and backend/operator path | Backend/operator path and evidence consumers | Accepted/rejected commands, transitions, audit trail. |
| `agv/denford/v1/health/heartbeat` | primarily outbound from edge | Edge control service | Backend/operator consumers | Liveness and connectivity evidence. |

## Publisher / Subscriber Roles
- Edge control service subscribes to all `cmd/*` topics and publishes all `state/*`, `event/*`, and `health/heartbeat`.
- Backend/operator path publishes operator-originated commands and consumes state, telemetry, alarms, faults, audits, and heartbeat.
- MQTT broker only transports messages and does not perform business validation.

## QoS Policy
| Topic Class | QoS | Rationale |
| --- | --- | --- |
| `cmd/manual` | 1 | Delivery confirmation matters; duplicates must be tolerated via `msg_id`. |
| `cmd/mode` | 1 | Mode changes require reliable delivery and idempotent handling. |
| `cmd/reset` | 1 | Reset commands must be acknowledged or rejected explicitly. |
| `state/status` | 1 | Current state is critical and should survive transient network loss better than QoS 0. |
| `state/telemetry` | 0 | Periodic stream; latest values matter more than guaranteed replay. |
| `event/alarm` | 1 | Alarm evidence must be delivered reliably. |
| `event/fault` | 1 | Fault evidence must be delivered reliably. |
| `event/audit` | 1 | Command audit trail should be retained reliably. |
| `health/heartbeat` | 0 | Frequent liveness signal, lightweight by design. |

## Retained Policy
| Topic | Retained | Policy |
| --- | --- | --- |
| `cmd/manual` | No | Commands must not replay on reconnect. |
| `cmd/mode` | No | Commands must not replay on reconnect. |
| `cmd/reset` | No | Reset commands must not replay on reconnect. |
| `state/status` | Yes | Latest authoritative state should be available to late subscribers. |
| `state/telemetry` | No | Telemetry is time-series data, not retained snapshot state. |
| `event/alarm` | No | Events are historical records, not retained command/state. |
| `event/fault` | No | Events are historical records, not retained command/state. |
| `event/audit` | No | Audit trail should be persisted downstream, not retained in broker. |
| `health/heartbeat` | No | Heartbeat freshness depends on publication time. |

## JSON Payload Schema
All V1 MQTT payloads are JSON objects with the following contract fields:

```json
{
  "msg_id": "uuid-or-equivalent-unique-id",
  "ts": "2026-03-22T12:00:00Z",
  "source": "edge|backend|operator",
  "type": "command|status|telemetry|alarm|fault|audit|heartbeat",
  "mode": "INIT|IDLE|MANUAL|AUTO_LINE|SAFE_STOP|ESTOP_LATCHED|FAULT|DISCONNECTED_DEGRADED|MAINTENANCE",
  "state": "INIT|IDLE|MANUAL|AUTO_LINE|SAFE_STOP|ESTOP_LATCHED|FAULT|DISCONNECTED_DEGRADED|MAINTENANCE",
  "severity": "info|warning|critical",
  "payload": {},
  "corr_id": "optional-correlation-id",
  "ack_required": true
}
```

## Required Field Rules
- `msg_id`: mandatory for all messages; used for deduplication and evidence traceability.
- `ts`: mandatory UTC timestamp.
- `source`: mandatory origin identifier.
- `type`: mandatory message class.
- `mode`: mandatory for commands that request mode context and for all state/status publications.
- `state`: mandatory for status, alarm, fault, audit, and heartbeat messages that reflect controller state.
- `severity`: mandatory for event, fault, alarm, and audit outcomes; commands may use `info`.
- `payload`: mandatory object containing topic-specific data.
- `corr_id`: required for acknowledgements, command outcomes, and linked event chains.
- `ack_required`: required for all `cmd/*` topics; optional false for state/event/telemetry messages.

## Topic-Specific Payload Expectations

### `cmd/manual`
```json
{
  "msg_id": "cmd-001",
  "ts": "2026-03-22T12:00:00Z",
  "source": "operator",
  "type": "command",
  "mode": "MANUAL",
  "state": "IDLE",
  "severity": "info",
  "payload": {
    "linear": 0.2,
    "angular": 0.0,
    "duration_ms": 500
  },
  "corr_id": "op-001",
  "ack_required": true
}
```

### `cmd/mode`
```json
{
  "msg_id": "cmd-010",
  "ts": "2026-03-22T12:00:02Z",
  "source": "operator",
  "type": "command",
  "mode": "AUTO_LINE",
  "state": "IDLE",
  "severity": "info",
  "payload": {
    "requested_mode": "AUTO_LINE",
    "reason": "operator_request"
  },
  "corr_id": "op-002",
  "ack_required": true
}
```

### `state/status`
```json
{
  "msg_id": "state-101",
  "ts": "2026-03-22T12:00:03Z",
  "source": "edge",
  "type": "status",
  "mode": "AUTO_LINE",
  "state": "AUTO_LINE",
  "severity": "info",
  "payload": {
    "prev_state": "IDLE",
    "transition_reason": "mode_auto_line_requested",
    "traction_enabled": true
  },
  "corr_id": "op-002",
  "ack_required": false
}
```

### `event/alarm` and `event/fault`
```json
{
  "msg_id": "evt-501",
  "ts": "2026-03-22T12:00:10Z",
  "source": "edge",
  "type": "alarm",
  "mode": "AUTO_LINE",
  "state": "SAFE_STOP",
  "severity": "warning",
  "payload": {
    "code": "obstacle_detected",
    "description": "Protective stop due to obstacle input"
  },
  "corr_id": "op-002",
  "ack_required": false
}
```

## Command Acknowledgement / Timeout / Reject Semantics
- Every command on `cmd/*` with `ack_required=true` must produce an `event/audit` result referencing the original `msg_id` in `corr_id`.
- Accepted commands must also be reflected by `state/status` if they cause a state transition.
- Rejected commands must include:
  - `result = rejected`
  - `reason_code`
  - `current_state`
  - `requested_action`
- If no acceptance or rejection evidence is produced within the command timeout budget, the backend/operator path must treat the command as timed out and non-authoritative.
- Timeout budgets are contract-level defaults:
  - `cmd/manual`: 1000 ms
  - `cmd/mode`: 2000 ms
  - `cmd/reset`: 3000 ms

## Illegal Transition Handling
- If a command requests a forbidden transition, the edge controller must reject it.
- Rejection must publish `event/audit` with `severity=warning` or `severity=critical` depending on context.
- If the illegal transition indicates unsafe or inconsistent internal state, an additional `event/fault` must be published.
- Illegal commands must never directly change controller state.

## Heartbeat Policy
- Edge publishes `agv/denford/v1/health/heartbeat` at a nominal 1 Hz cadence.
- Each heartbeat includes controller state, current mode, and link health summary in `payload`.
- If heartbeat age exceeds 3 seconds on the consumer side, communications must be treated as degraded.
- If heartbeat loss affects motion-capable states, the controller must transition to `DISCONNECTED_DEGRADED` and then to `SAFE_STOP` if uncertainty persists.
