# MVP Freeze Checklist

## Frozen MVP includes
- Stage 1 contract documents in `06_engineering/06_00_contract/`.
- Stage 2 functional twin and mandatory scenario evidence.
- Stage 3 hardware-agnostic edge runtime MVP.
- Stage 4 real local MQTT transport path.
- Stage 5 backend MVP with MQTT ingest, dev/demo storage, REST, and WebSocket.
- Stage 6 operator-facing lightweight console path.
- Stage 7 repeatable integration runner and freeze documentation.

## Frozen MVP does not include
- GPIO or Raspberry Pi specific runtime code.
- Real AGV wiring and motor/sensor binding.
- Webots integration.
- Heavy frontend UI.
- Production deployment packaging.
- Lab-side hardware validation evidence.

## Finished enough before lab trip
- Local full chain is repeatable.
- Contract-level scenarios are evidenced end-to-end.
- Backend and operator paths expose observable evidence.
- MVP scope is explicitly frozen to avoid uncontrolled changes before hardware phase.

## Must remain unchanged before hardware phase
- Topic namespace and message shape at contract level.
- State machine semantics already evidenced in software-only path.
- Edge/backend/operator boundary responsibilities.
- Board-agnostic adapter strategy.

## Still open but intentionally deferred
- Exact board binding details.
- Hardware adapter implementation.
- GPIO pin mapping and wiring survey.
- Real AGV safety I/O confirmation.
- Final deployment decisions for lab/hardware phase.
