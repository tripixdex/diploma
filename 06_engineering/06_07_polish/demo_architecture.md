# Demo Architecture

## Purpose
- Stage 7B does not introduce a new system layer.
- It wraps the already frozen software-only MVP into one polished, repeatable demo path.

## Demo composition
- `operator` layer sends commands and receives live updates.
- `backend` layer stores commands, events, status, and telemetry, and exposes REST/WebSocket access.
- `transport` layer carries MQTT messages through a local broker-backed path.
- `edge` layer applies command handling, heartbeat supervision, degraded behavior, and local safety decisions.
- `integration` layer remains the authoritative end-to-end orchestration engine.
- `polish` layer adds demo narrative, freeze artifacts, and supervisor-facing walkthrough material.

## State of authority
- Contract semantics remain defined by `06_engineering/06_00_contract/`.
- Runtime behavior remains implemented by Stages 2 through 7.
- Stage 7B only repackages the software-only contour for a stable demonstration.

## Demo execution path
1. Start the local software-only chain.
2. Show initial status visibility.
3. Send operator mode command.
4. Send operator manual command.
5. Show edge reaction through MQTT.
6. Show backend persistence and operator live update.
7. Show heartbeat timeout and degraded transition.
8. Show invalid command rejection.
9. End with a clear summary of what is proven and what is still deferred.

## Explicit non-goals
- No board binding.
- No GPIO.
- No real AGV wiring.
- No Webots.
- No heavy frontend.
