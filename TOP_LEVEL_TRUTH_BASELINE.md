# Top Level Truth Baseline

## What Is Actually Implemented Now
- Contract documents that define states, commands, MQTT topics, and acceptance boundaries.
- A functional software twin that runs the contract logic locally.
- A hardware-agnostic edge MVP with command intake, heartbeat supervision, degraded behavior, and local command rejection.
- A real local MQTT transport contour for software-only exchange.
- A backend MVP with MQTT ingest, dev/demo storage, REST API, and WebSocket live stream.
- An operator path and human UI for software-only observation and command dispatch.
- Repeatable software-only integration runner and polished demo runner.

## What Is Actually Evidenced Now
- Contract-level scenarios in the twin are evidenced.
- End-to-end software-only flow `operator -> backend -> MQTT -> edge -> MQTT -> backend -> operator` is evidenced locally.
- MQTT message exchange is evidenced in a local demo contour.
- Backend observation, storage path, REST, and WebSocket behavior are evidenced in dev/demo mode.
- Human UI is evidenced as a software-only operator/demo surface over the existing backend path.

## What Is Explicitly Deferred
- Webots scene/model integration.
- PostgreSQL as the currently evidenced runtime storage backend.
- Docker Compose deployment and reproducible full-stack packaging.
- Mosquitto deployment validation as the current deployment baseline.
- Raspberry Pi binding, GPIO, board-specific deployment, and real AGV wiring.
- Any claim of proven safety on real hardware.

## What Must Not Be Claimed
- That the repo is hardware-ready.
- That Raspberry Pi 4 runtime binding is already implemented or validated.
- That Orange Pi portability is implemented.
- That safety contour behavior is proven on the real AGV.
- That PostgreSQL, Docker Compose, Webots, or Mosquitto deployment are already evidenced if the current proof is only local/dev/demo or still deferred.
- That the project is production-ready.

## Current Honest Entry Point To Hardware Readiness
- Hardware readiness is still blocked.
- The current honest entry point is a future hardware phase that starts only after board facts, wiring, safety contour, power, and I/O interfaces are physically surveyed and documented.
- The current repo proves a software-only MVP contour and pre-hardware preparation, not a deployed AGV modernization on real hardware.
