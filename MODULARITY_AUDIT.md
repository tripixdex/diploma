# Modularity Audit

## Scope

- Audited active contract-driven simulation code in `06_engineering/06_01_sim_twin/`.
- This is an architectural audit only; no Stage 3 implementation is introduced here.

## Findings

| Module / File | Issue | Severity | Why It Matters | Recommended Fix | Must Fix Before Stage 3? |
| --- | --- | --- | --- | --- | --- |
| `06_engineering/06_01_sim_twin/twin_state_machine.py` | State machine mixes transition authority, context mutation, safety reactions, and publish-side effects in one class | High | Future edge runtime will need domain transitions independent from transport/output adapters; current coupling makes that swap risky | Split pure transition logic from side-effect emission, e.g. transition engine + effect mapper + publisher adapter | YES |
| `06_engineering/06_01_sim_twin/twin_state_machine.py` + `twin_publishers.py` | `TwinStateMachine` depends on concrete `InMemoryPublisher`, not on a narrow publisher interface | High | Blocks clean substitution with a future MQTT-backed publisher or test spy without touching state logic | Introduce a publisher protocol/interface and keep `InMemoryPublisher` as one implementation | YES |
| `06_engineering/06_01_sim_twin/twin_scenarios.py` | Scenario file combines reusable demo flows, acceptance execution, pass/fail assertions, and evidence formatting | Medium | Responsibility sprawl makes the file the de facto orchestration center and will become harder to extend for Stage 3 tests | Split into scenario definitions, scenario assertions, and scenario reporting helpers | YES |
| `06_engineering/06_01_sim_twin/run_twin_demo.py` and `run_stage2_scenarios.py` | Runner scripts own import bootstrapping via `sys.path` mutation | Medium | Entry scripts are doing package-environment work instead of just invoking application logic | Convert twin folder into a clean package entrypoint model and run via `python -m` | YES |
| `06_engineering/06_01_sim_twin/twin_runtime.py` | Runtime prints transitions directly to console | Low | Runtime orchestration and presentation/log output are coupled | Route output through an injected logger or a reporting callback | NO |
| `06_engineering/06_01_sim_twin/twin_models.py` + `twin_scenarios.py` | State and event enums are centralized, but scenario expectations are re-expressed manually as strings | Medium | Logic is partially centralized, but evidence text is not derived from the same authority | Add a small scenario expectation helper layer that renders from enums/constants | NO |
| `06_engineering/06_01_sim_twin/` overall | No explicit config boundary exists between state logic, publisher contract literals, and runner behavior | High | Stage 3 will require environment/config injection for edge runtime without rewriting multiple modules | Add a dedicated config/constants module before edge work starts | YES |
| `06_engineering/06_01_sim_twin/` overall | No cyclic imports were found, and current module graph is still understandable | Low | This is a positive finding, but it can regress quickly once transport/runtime code is added | Preserve one-way dependency flow: models -> state logic -> runtime -> runners | NO |

## Boundary Assessment

### Present boundaries that already exist
- `twin_models.py` centralizes core enums and dataclasses.
- `twin_events.py` isolates fake event creation.
- `twin_publishers.py` isolates in-memory publication mechanics.
- `twin_runtime.py` orchestrates a runtime instance instead of embedding transition rules itself.

### Weak boundaries that will hurt Stage 3 if left unchanged
- Publisher abstraction is not formal; only one concrete class is known to the state machine.
- Contract literals are spread between publisher and scenario code.
- State machine emits side effects directly instead of returning structured effects.
- Runner scripts are package/bootstrap aware, which is the wrong layer.

## Summary

- The twin is modular enough for Stage 2 and remains understandable.
- It is not yet modular enough for safe Stage 3 edge work.
- Pre-Stage-3 must-fix set is architectural, not feature-driven:
  - introduce shared config/constants;
  - define publisher interface boundaries;
  - separate pure transition logic from publish/log side effects;
  - reduce responsibility sprawl in `twin_scenarios.py`;
  - remove runner `sys.path` hacks.
