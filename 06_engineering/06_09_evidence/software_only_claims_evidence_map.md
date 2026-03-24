# Software-Only Claims Evidence Map

| Claim | Evidence Now | Evidence Source | Claim Status |
| --- | --- | --- | --- |
| Contract-aligned software twin exists | Yes | `../06_01_sim_twin/stage2_scenario_evidence.md` | EVIDENCED |
| Hardware-agnostic edge runtime exists | Yes | `artifacts/integration_full_chain.log`; `../06_02_edge/edge_architecture.md` | EVIDENCED |
| Real local MQTT exchange exists | Yes | `artifacts/integration_full_chain.log`; `artifacts/backend_demo_ingest.log` | EVIDENCED |
| Backend MQTT ingest, REST, and WebSocket exist | Yes | `artifacts/backend_demo_ingest.log`; `artifacts/backend_health.json` | EVIDENCED |
| Human UI path exists | Yes | `artifacts/ui_http_head.txt`; `artifacts/ui_smoke_summary.json` | EVIDENCED |
| Full-chain software-only contour is repeatable | Yes | `artifacts/integration_full_chain.log`; `artifacts/polished_demo_summary.log` | EVIDENCED |
| Storage is proven as PostgreSQL runtime | No | No matching runtime artifact | DEFERRED / MUST NOT CLAIM |
| Docker deployment exists and is validated | No | No matching runtime artifact | DEFERRED / MUST NOT CLAIM |
| Webots simulation is implemented and evidenced | No | No matching runtime artifact | DEFERRED / MUST NOT CLAIM |
| Mosquitto deployment baseline is validated | No | No matching deployment artifact | DEFERRED / MUST NOT CLAIM |
| Raspberry Pi runtime binding is implemented | No | No board-binding artifact | DEFERRED / MUST NOT CLAIM |
| Hardware readiness gate is open | No | `../../TOP_LEVEL_TRUTH_BASELINE.md` | MUST NOT CLAIM |
| Real AGV safety is proven | No | No hardware safety artifact | MUST NOT CLAIM |
