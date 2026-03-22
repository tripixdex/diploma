# Twin Architecture

## Module Set
- `twin_models.py`: enums and dataclasses for state, mode, events, runtime context, and published messages.
- `twin_events.py`: event factory helpers for scenario and command generation.
- `twin_publishers.py`: in-memory publisher stub that stores and prints contract-shaped messages.
- `twin_state_machine.py`: authoritative transition rules and transition handling.
- `twin_runtime.py`: runtime loop facade that applies events and snapshots context.
- `twin_scenarios.py`: predefined scenario runners aligned to Stage 1 acceptance scenarios.
- `run_twin_demo.py`: minimal local demo entrypoint.

## Event Loop / Runtime Loop
The twin uses a simple local event loop:
1. create runtime context in `INIT`;
2. accept one event at a time;
3. evaluate transition legality in the state machine;
4. update authoritative state if transition is allowed;
5. emit fake status, audit, alarm, fault, telemetry, or heartbeat messages;
6. keep all messages in memory for later inspection.

This loop is deterministic and synchronous by design. Stage 2 is validating contract logic, not concurrency, transport, or performance behavior.

## State Authority
The edge-like twin state machine is the single authority. Commands do not directly mutate outputs. They are translated into events and validated against current state, safety flags, and transition rules before the state changes.

## Simulated Sensors
The twin models logical signals only:
- line presence and line loss;
- docking completion;
- obstacle detection;
- e-stop active;
- link/heartbeat degraded.

These are represented as event triggers and runtime flags, not as real GPIO or hardware drivers.

## Simulated Command Intake
The twin accepts logical command events equivalent to:
- mode requests;
- manual motion requests;
- safe-stop requests;
- reset requests;
- maintenance requests.

Command intake is local and synchronous. There is no broker and no network stack at Stage 2.

## MQTT Publishing Abstraction
The publisher layer is a stub that formats messages using the Stage 1 topic structure and stores them in memory. It is intentionally transport-free:
- no broker session;
- no QoS negotiation;
- no retained message behavior in a real broker.

What exists now is only the publication contract surface needed for Stage 2 validation.

## Why Twin Is Hardware-Agnostic
The twin depends only on logical signals and contract states. It does not know any GPIO numbers, Raspberry Pi revision, motor driver interface, or real sensor wiring. That separation is deliberate so Stage 3 can later attach a hardware-aware edge layer without rewriting the contract logic from scratch.
