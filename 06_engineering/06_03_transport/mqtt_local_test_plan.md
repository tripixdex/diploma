# MQTT Local Test Plan

## Stage 4 Purpose
Validate the first real MQTT-backed exchange locally without backend, UI, Docker full stack, Webots, or hardware integration.

## Mandatory Checks
- local broker starts;
- edge gateway connects and subscribes to `cmd/*`;
- operator publisher connects and publishes contract-shaped commands;
- edge side consumes commands and publishes contract-shaped status/event/heartbeat messages;
- observer client receives those messages;
- late observer receives retained `state/status`;
- operator reconnect and continued publish flow work in the same broker session;
- Stage 2 and Stage 3 demos remain operational after Stage 4 changes.

## Explicitly Out of Scope
- backend persistence;
- UI workflows;
- Raspberry Pi GPIO;
- broker deployment automation;
- hardware timing claims;
- Webots integration.

## Validation Commands
- `python3 -m py_compile 06_engineering/06_03_transport/*.py`
- `python3 06_engineering/06_03_transport/mqtt_transport_runner.py`
- `python3 06_engineering/06_01_sim_twin/run_twin_demo.py`
- `python3 06_engineering/06_01_sim_twin/run_stage2_scenarios.py`
- `python3 06_engineering/06_02_edge/edge_demo_runner.py`
