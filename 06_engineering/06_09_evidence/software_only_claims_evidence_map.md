# Software-Only Claims Evidence Map

| Claim | Evidence Now | Primary Provenance Artifact(s) | Claim Status |
| --- | --- | --- | --- |
| Contract-aligned software twin exists | Yes | `../06_01_sim_twin/stage2_scenario_evidence.md`; `../../MINIMAL_REGRESSION_BASELINE.md` | EVIDENCED |
| Hardware-agnostic edge runtime exists | Yes | `artifacts/logs/20260326T001703+0300__integration_full_chain.log`; `../06_02_edge/edge_architecture.md` | EVIDENCED |
| Real local MQTT exchange exists | Yes | `artifacts/logs/20260326T001703+0300__integration_full_chain.log`; `artifacts/logs/20260326T001703+0300__backend_demo_ingest.log` | EVIDENCED |
| Backend MQTT ingest, REST, and WebSocket exist | Yes | `artifacts/logs/20260326T001703+0300__backend_demo_ingest.log`; `artifacts/http_ws/20260326T001703+0300__backend_health.json` | EVIDENCED |
| Human UI path exists | Yes | `artifacts/ui/20260326T001703+0300__ui_proof_summary.md`; `artifacts/http_ws/20260326T001703+0300__ui_http_head.txt`; `artifacts/ui/20260326T001703+0300__ui_smoke_output.txt` | EVIDENCED |
| Full-chain software-only contour is repeatable | Yes | `artifacts/logs/20260326T001703+0300__integration_full_chain.log`; `artifacts/summaries/20260326T001703+0300__polished_demo_summary.log` | EVIDENCED |
| Storage is proven as PostgreSQL runtime | No | No matching runtime artifact | DEFERRED / MUST NOT CLAIM |
| Docker deployment exists and is validated | No | No matching deployment artifact | DEFERRED / MUST NOT CLAIM |
| Webots simulation is implemented and evidenced | No | No matching runtime artifact | DEFERRED / MUST NOT CLAIM |
| Mosquitto deployment baseline is validated | No | No matching deployment artifact | DEFERRED / MUST NOT CLAIM |
| Raspberry Pi runtime binding is implemented | No | No board-binding artifact | DEFERRED / MUST NOT CLAIM |
| Orange Pi portability is proven | No | No portability artifact | DEFERRED / MUST NOT CLAIM |
| Hardware readiness gate is open | No | `../../TOP_LEVEL_TRUTH_BASELINE.md`; `../06_10_policy/hardware_entry_gate.md` | MUST NOT CLAIM |
| Real AGV safety is proven | No | No hardware safety artifact | MUST NOT CLAIM |
