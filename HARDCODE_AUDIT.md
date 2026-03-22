# Hardcode Audit

## Scope

- Audited active simulation code in `06_engineering/06_01_sim_twin/`.
- Archive, NIRS, VKR-history, and legacy source zones were not refactored.

## Findings

| File | Line / Location | What Is Hardcoded | Why This Is Bad | Severity | Recommended Fix | Must Fix Before Stage 3? |
| --- | --- | --- | --- | --- | --- | --- |
| `06_engineering/06_01_sim_twin/twin_publishers.py` | `35-88` | MQTT topic names like `agv/denford/v1/state/status`, `.../event/audit`, `.../health/heartbeat` are repeated as raw strings | Stage 3 transport integration will duplicate and drift from the contract if topics stay embedded in publisher methods | High | Move topic names into a dedicated contract/config constants module shared by twin and future edge runtime | YES |
| `06_engineering/06_01_sim_twin/twin_publishers.py` | `14-27` | Message ID pattern `sim-{seq:04d}`, `ts=\"SIM_TIME\"`, `ack_required=False`, default `severity=\"info\"` are baked into publish path | Prevents swapping simulation message shaping to edge/runtime message shaping without editing internals | Medium | Introduce a message factory or transport config object for IDs, timestamps, severity defaults, and ack policy | YES |
| `06_engineering/06_01_sim_twin/twin_state_machine.py` | `93-100` | Telemetry values `line_detected` and `dock_complete` are embedded in state transition side effects | Real sensor semantics will diverge from these placeholder literals and force code edits in state logic | Medium | Replace raw literals with symbolic telemetry constants or scenario-provided payload builders | YES |
| `06_engineering/06_01_sim_twin/run_twin_demo.py` | `7-9` | Runtime modifies `sys.path` using local filesystem path | Environment-dependent bootstrap logic is fragile and will break when code is packaged differently | Medium | Use package execution (`python -m ...`) or a dedicated package entrypoint instead of path hacking | YES |
| `06_engineering/06_01_sim_twin/run_stage2_scenarios.py` | `7-9` | Same `sys.path` mutation pattern | Repeats environment-coupled bootstrap logic in a second runner | Medium | Use the same package entrypoint strategy for all runners | YES |
| `06_engineering/06_01_sim_twin/twin_events.py` | `5,9,13,17,21,25,29,33,37,41,45,51,59` | Event source labels `system`, `operator`, `sensor` are hardcoded in each factory | Future integration with edge/runtime adapters may need source authority mapping in one place, not scattered per helper | Low | Centralize source labels in constants or an event factory layer | NO |
| `06_engineering/06_01_sim_twin/twin_scenarios.py` | `84-87`, `111-115`, `138-142`, `166-170`, `195-199`, `225-228`, `253-256`, `277` | Topic expectations are duplicated as raw string lists in scenario assertions | Test evidence becomes brittle if contract topic names change once | Medium | Reuse a shared topic registry/constants module in scenario assertions | YES |
| `06_engineering/06_01_sim_twin/twin_scenarios.py` | `91-97`, `119-126`, `146-153`, `174-181`, `204-210`, `233-240`, `261-267`, `280-287` | State names and expected transitions are duplicated as plain strings in scenario result text | Human-readable evidence and code logic can diverge | Low | Build expected transition text from enums/constants where practical | NO |
| `06_engineering/06_01_sim_twin/twin_scenarios.py` | `106`, `47`; `run_twin_demo.py:18` | Manual command magnitudes `0.2` and `0.0` are magic numbers in demo/scenario flow | Acceptable for demo, but undocumented values become noise when motion profiles appear | Low | Move demo motion values into named scenario constants | NO |
| `06_engineering/06_01_sim_twin/twin_state_machine.py` | `108`, `111`, `115`; `50` | Audit reasons like `illegal_transition`, `manual_command_accepted`, `manual_command_blocked_by_safety` are hardcoded strings | Contract-aligned audit taxonomy is not centralized and can drift between twin and future edge runtime | Medium | Define audit reason constants or enums shared by publishers and state logic | YES |

## Summary

- The most important hardcode cluster is not numeric; it is contract literal duplication.
- The current twin is acceptable for Stage 2, but Stage 3 should not start with topic names, audit reasons, bootstrap paths, and message-shaping defaults spread across modules.
- Highest-priority pre-Stage-3 fixes: centralize topic constants, remove `sys.path` bootstrap hacks, and extract message/audit literal policy out of `twin_publishers.py` and `twin_state_machine.py`.
