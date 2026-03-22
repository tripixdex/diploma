# MQTT Topics Manifest

The Stage 4 transport demo uses the Stage 1 V1 namespace:

`agv/denford/v1/`

## Command Topics
| Topic | QoS | Retained | Purpose |
| --- | --- | --- | --- |
| `agv/denford/v1/cmd/manual` | 1 | No | Manual bounded motion command to edge runtime. |
| `agv/denford/v1/cmd/mode` | 1 | No | Mode transition requests to edge runtime. |
| `agv/denford/v1/cmd/reset` | 1 | No | Reset requests for safe stop, e-stop, or fault recovery. |

## State / Event Topics
| Topic | QoS | Retained | Purpose |
| --- | --- | --- | --- |
| `agv/denford/v1/state/status` | 1 | Yes | Latest authoritative edge state. |
| `agv/denford/v1/state/telemetry` | 0 | No | Telemetry snapshots. |
| `agv/denford/v1/event/alarm` | 1 | No | Alarm evidence. |
| `agv/denford/v1/event/fault` | 1 | No | Fault evidence. |
| `agv/denford/v1/event/audit` | 1 | No | Accepted/rejected command evidence. |
| `agv/denford/v1/health/heartbeat` | 0 | No | Liveness and degraded-link evidence. |

## Stage 4 Demo Use
- Operator-side publisher sends `cmd/mode` and `cmd/manual`.
- Edge transport gateway consumes all `cmd/*`.
- Edge transport gateway publishes `state/status`, `state/telemetry`, `event/audit`, `event/alarm`, and `health/heartbeat`.
- A late observer subscribes to `state/status` to verify retained-state behavior.
