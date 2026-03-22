# Stage 2 Test Plan

## What We Check in Stage 2
- the twin runtime starts locally;
- the state machine exists in code and applies real transitions;
- fake command and sensor events can drive contract-aligned state changes;
- in-memory publication log captures status, audit, alarm, fault, telemetry, and heartbeat messages;
- mandatory Stage 1 scenarios are representable in code-level scaffold form.

## What We Do Not Check in Stage 2
- real MQTT broker behavior;
- backend ingestion;
- operator UI;
- Webots world or visual scene;
- Raspberry Pi GPIO or motor control;
- hardware timing or physical robot motion.

## Mandatory Scenarios Before Stage 2 Closeout
- startup;
- manual mode;
- obstacle to safe stop;
- safe stop clear back to idle;
- auto line completion to idle;
- e-stop latch and reset path;
- link loss to degraded path;
- invalid command rejection.

## Mandatory Execution Method
- run `python3 06_engineering/06_01_sim_twin/run_stage2_scenarios.py`;
- verify that all mandatory scenarios report `PASS`;
- record the resulting evidence in `06_engineering/06_01_sim_twin/stage2_scenario_evidence.md`;
- do not claim Stage 2 closeout if any mandatory scenario is missing or fails.
