# Release Manifest

## Active software-only parts
- `06_engineering/06_00_contract/`: contract and MVP boundaries.
- `06_engineering/06_01_sim_twin/`: functional twin and contract-level scenario evidence.
- `06_engineering/06_02_edge/`: local edge MVP.
- `06_engineering/06_03_transport/`: real local MQTT transport.
- `06_engineering/06_04_backend/`: backend MVP.
- `06_engineering/06_05_operator/`: operator-facing console path.
- `06_engineering/06_06_integration/`: repeatable integration evidence and MVP freeze.

## Source of truth directories
- System contract: `06_engineering/06_00_contract/`
- Domain/state behavior: `06_engineering/06_01_sim_twin/`
- Edge runtime: `06_engineering/06_02_edge/`
- MQTT transport: `06_engineering/06_03_transport/`
- Backend/API/storage: `06_engineering/06_04_backend/`
- Operator path: `06_engineering/06_05_operator/`
- Integration evidence and freeze: `06_engineering/06_06_integration/`

## What is demonstrated in software-only phase
- End-to-end command/status/event/telemetry flow.
- Local degraded behavior on heartbeat loss.
- Backend persistence and serving path.
- Operator observation and command dispatch path.
- Repeatable evidence without hardware-specific claims.

## What to show supervisor / pre-defense
- Stage 1 contract documents.
- Stage 2 scenario evidence.
- Stage 7 integration runner output.
- Stage 5 backend path and Stage 6 operator path logs.
- Stage 7 MVP freeze checklist and board target strategy.
