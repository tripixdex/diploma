# Integration Architecture

## Purpose
- Provide one repeatable software-only contour that proves the active modules work together without hardware-specific code.

## Active chain
1. `operator_commands` publishes contract-shaped MQTT commands.
2. Stage 4 transport receives commands and maps them into Stage 3 edge runtime actions.
3. Stage 3 edge runtime emits status, telemetry, audit, alarm, and heartbeat messages.
4. Stage 5 backend bridge ingests MQTT traffic and stores command/event/status/telemetry evidence.
5. Stage 6 operator clients read current data through REST and live frames through WebSocket.

## Boundaries
- Stage 2 remains the domain/state-machine source of truth.
- Stage 3 remains the edge runtime source of truth.
- Stage 4 remains the MQTT transport source of truth.
- Stage 5 remains the backend/API/storage source of truth.
- Stage 6 remains the operator-facing client source of truth.
- Stage 7 adds orchestration, repeatable evidence, and freeze documentation only.

## Why this is the freeze contour
- It is the strongest currently evidenced software-only path.
- It is board-agnostic.
- It can be rerun locally before any lab trip.
- It provides concrete evidence for VKR without inventing hardware claims.
