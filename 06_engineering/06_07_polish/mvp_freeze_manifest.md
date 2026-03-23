# MVP Freeze Manifest

## Frozen software MVP includes
- System contract documents in `06_engineering/06_00_contract/`.
- Functional twin in `06_engineering/06_01_sim_twin/`.
- Edge MVP in `06_engineering/06_02_edge/`.
- MQTT transport in `06_engineering/06_03_transport/`.
- Backend MVP in `06_engineering/06_04_backend/`.
- Operator path in `06_engineering/06_05_operator/`.
- Repeatable integration evidence in `06_engineering/06_06_integration/`.
- Stage 7B polished demo and pre-hardware preparation artifacts in `06_engineering/06_07_polish/`.
- This frozen contour is software-only and demo-grade, not hardware-ready and not production-ready.

## Implemented runtime subset
- Active states in the current software-only MVP: `INIT`, `IDLE`, `MANUAL`, `AUTO_LINE`, `SAFE_STOP`, `ESTOP_LATCHED`, `FAULT`, `DISCONNECTED_DEGRADED`.
- Active operator commands: `cmd/mode` for `MANUAL` and `AUTO_LINE`, bounded `cmd/manual`, and state-validated `cmd/reset`.
- Active degraded behavior: initial `DISCONNECTED_DEGRADED`, then `SAFE_STOP` if disconnect persists beyond the grace window.

## Must not change before hardware phase
- Contract-level topic namespaces without explicit contract revision.
- Message shape fundamentals already frozen in Stage 1 and exercised in Stages 4 through 7.
- Core state semantics and degraded behavior semantics.
- Separation between edge, transport, backend, operator, and integration layers.
- Honest positioning of the current contour as software-only.

## Intentionally deferred
- `MAINTENANCE` state and maintenance-only transitions.
- GPIO and board-specific runtime.
- Raspberry Pi 4 binding details.
- Orange Pi portability work.
- Real AGV wiring and I/O mapping.
- Webots integration.
- PostgreSQL as the evidenced current runtime storage backend.
- Docker Compose deployment and full-stack packaging.
- Deployment-grade Mosquitto validation.
- Heavy UI or product-level operator console.

## Source of truth
- Contract: `06_engineering/06_00_contract/`
- Runtime contour: `06_engineering/06_01_sim_twin/` through `06_engineering/06_06_integration/`
- Execution status: `99_reports/execution/`
- Stage 7B packaging and demo guidance: `06_engineering/06_07_polish/`
