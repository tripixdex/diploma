# Functional Digital Twin

## What It Is
This Stage 2 directory contains a minimal functional digital twin of AGV Denford. It is a software runtime that applies the Stage 1 contract as executable logic: states, events, transitions, fake sensors, and fake message publication.

## What It Can Do
- run a local authoritative state machine;
- accept fake command and sensor events;
- simulate key Stage 1 scenarios such as startup, manual mode, safe stop, e-stop, link loss, docking, and invalid command rejection;
- publish contract-shaped fake messages through an in-memory publisher;
- print a demo transition trace without requiring broker, backend, UI, hardware, or Webots.

## What It Does Not Do
- no real MQTT transport;
- no Webots scene;
- no backend or operator UI;
- no GPIO, motor driver, or real sensor integration;
- no hardware adapter implementation;
- no claim of physical robot runtime behavior.

## Relation to Contract Docs
This twin is derived from:
- `06_engineering/06_00_contract/SYSTEM_CONTRACT.md`
- `06_engineering/06_00_contract/STATE_MACHINE.md`
- `06_engineering/06_00_contract/IO_MAP.md`
- `06_engineering/06_00_contract/MQTT_CONTRACT.md`
- `06_engineering/06_00_contract/ACCEPTANCE_CRITERIA.md`

The twin is intentionally contract-first: if runtime behavior and contract diverge, the contract must be reviewed explicitly.

## Why This Is Stage 2
This is still a simulation-first scaffold, not a real robot runtime. The goal is to prove that the contract can execute in software before any Stage 3 edge implementation, MQTT transport, or hardware-specific logic is introduced.
