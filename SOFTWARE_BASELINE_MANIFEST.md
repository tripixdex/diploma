# Software Baseline Manifest

## Included In The Canonical Software Baseline
- Local embedded MQTT-backed transport used by the software-only runtime
- Hardware-agnostic edge runtime
- Backend runtime with dev/demo storage, REST, and WebSocket
- Human UI over the existing backend path
- Shared runtime bootstrap utility in `06_engineering/runtime_bootstrap.py`

## Canonical Entrypoints
- Full baseline runtime:
  - `python3 06_engineering/06_08_ui/ui_demo_stack.py`
- Canonical verification path:
  - `python3 06_engineering/06_06_integration/integration_runner.py`

## Supporting Entrypoints Only
- `python3 06_engineering/06_07_polish/demo_runner.py`
  - demo wrapper for presentation flow
- `python3 06_engineering/06_04_backend/backend_demo_runner.py`
  - backend proof path
- `python3 06_engineering/06_05_operator/operator_demo_runner.py`
  - operator proof path
- `python3 06_engineering/06_03_transport/mqtt_transport_runner.py`
  - transport proof path
- `python3 06_engineering/06_02_edge/edge_demo_runner.py`
  - edge-local proof path
- `python3 06_engineering/06_01_sim_twin/run_stage2_scenarios.py`
  - twin/state-machine proof path

## Out Of Scope
- Hardware phase
- Board binding
- GPIO
- Real AGV interface control
- Deployment packaging
- Docker Compose full-stack orchestration
- PostgreSQL runtime proof
- Deployment-grade Mosquitto proof
- Webots

## Why This Manifest Exists
- To remove ambiguity about which run path is authoritative
- To give reviewers one boring baseline instead of several overlapping demos
- To keep supporting/demo/internal runners available without presenting them as the primary project entrypoint
