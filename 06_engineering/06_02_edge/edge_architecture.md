# Edge Architecture

## Runtime Purpose
The Stage 3 edge runtime is the minimum onboard logic contour between external command/event intake and the contract-driven state machine. It is not a broker client, not a GPIO layer, and not a backend integration point.

## Main Modules
- `edge_models.py`: edge-facing command, runtime snapshot, and record structures.
- `edge_commands.py`: factory helpers for readable demo and local command creation.
- `edge_adapter_protocol.py`: explicit boundary between runtime and any external environment.
- `edge_runtime_config.py`: heartbeat timeout and default runtime parameters.
- `edge_heartbeat.py`: link supervision logic for degraded/disconnected behavior.
- `edge_runtime.py`: runtime coordinator, adapter bridge, local safety rejections, and reuse of Stage 2 domain logic.
- `edge_demo_runner.py`: local demonstration entrypoint.

## State Authority
Authoritative state transitions remain governed by the existing Stage 2 state machine logic. Stage 3 does not redefine the contract; it wraps that logic in an edge-oriented runtime boundary.

## Adapter Boundary
The runtime depends on `EdgeAdapterProtocol`, not on any real transport or hardware implementation. The adapter is responsible only for accepting emitted runtime records. At this stage, an in-memory adapter is used.

## Heartbeat Supervision
Heartbeat supervision is modeled locally through a dedicated link supervisor. When the timeout threshold is exceeded, the runtime generates a contract-aligned loss-link event and drives the domain into degraded behavior without requiring cloud participation.

## Local Safety Rejection
Unsafe commands are rejected locally before any hardware-specific action is considered. Examples:
- manual motion outside `MANUAL`;
- manual motion while obstacle/e-stop/link fault conditions are active;
- unsupported command types.

## Why Real Hardware Is Still Deferred
Exact Raspberry Pi revision and real Denford signal mapping remain unconfirmed. The Stage 3 MVP therefore keeps the edge contour hardware-agnostic and isolates future hardware binding behind the adapter boundary instead of faking GPIO integration prematurely.
