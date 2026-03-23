# Independent Expert Audit

## 1. Audit Scope
Evaluated:
- software-only MVP boundary in `06_engineering/`;
- contract set, edge/runtime, MQTT transport, backend MVP, operator path, UI, integration/demo evidence, freeze/pre-hardware artifacts;
- current reproducibility of key software-only checks.

Not evaluated:
- real hardware behavior;
- GPIO, wiring, board binding, motor drivers, sensor electrical semantics;
- real lab deployment;
- any claim that the project explicitly defers to hardware phase.

Current spot-checks performed during this audit:
- `python3 06_engineering/06_01_sim_twin/run_stage2_scenarios.py` -> passed `8/8`;
- `python3 06_engineering/06_02_edge/edge_demo_runner.py` -> passed;
- `python3 -m py_compile 06_engineering/06_04_backend/*.py 06_engineering/06_08_ui/ui_demo_stack.py` -> passed;
- `npm run build` in `06_engineering/06_08_ui/` -> passed;
- `python3 06_engineering/06_06_integration/integration_runner.py` -> failed during this audit because broker bind on `127.0.0.1:18884` was already occupied.

## 2. Executive Verdict
This is not a fake project. There is real software here.

But it is not cleanly ready for hardware phase. The project is strongest where it is honest about being software-only and weakest where it quietly overstates contract completeness, UI/operator trustworthiness, and repeatability of evidence.

Right now this is an acceptable software prototype with serious audit debt, not a strong pre-hardware package.

## 3. Scorecard
| Block | Score | Short verdict |
| --- | --- | --- |
| Engineering honesty | 3/5 | Mostly honest about no hardware claims, but not fully honest about what the software MVP actually proves. |
| Architecture quality | 2/5 | Layering exists on paper, but runtime composition is held together by dynamic import scaffolding and a reused twin state machine with side effects. |
| Hardcode / configuration discipline | 2/5 | Too many fixed ports, localhost assumptions, in-memory defaults, and demo-specific constants. |
| Modularity / maintainability | 2/5 | The repo is organized; the executable runtime is still brittle and overly demo-oriented. |
| Evidence quality | 2/5 | Evidence exists, but it is mostly self-generated, fragile, and not fully reproducible on demand. |
| UX / operator clarity | 2/5 | Screen is readable, but the command outcome logic is not trustworthy enough for operator proof. |
| Security / safety posture | 1/5 | Acceptable only for local MVP. Too weak to be treated as a serious operational contour. |
| Diploma strength | 3/5 | Better than a toy demo, weaker than a strong diploma-stage software package. |

## 4. What Is Actually Strong
- The project is disciplined in scope control. It repeatedly states that hardware work is not started and mostly avoids fake hardware claims.
- The software contour is real, not decorative: twin, edge, MQTT, backend, operator path, and browser UI all exist as code.
- The repository has unusually strong stage discipline and document hygiene for a student project.
- The state/event vocabulary is explicit and bounded. That is good diploma material if it is kept aligned to implementation.
- The UI is not just a static mockup. It is wired to REST and WebSocket paths and builds successfully.

## 5. What Is Weak or Fragile
- Contract and implementation are not fully aligned. The documents describe a richer controller than the executable software actually implements.
- The architecture is still demo-first, not clean-runtime-first. Dynamic module loading via `importlib.util.spec_from_file_location(...)` is everywhere: `06_02_edge/edge_runtime.py`, `06_03_transport/mqtt_transport_runner.py`, `06_04_backend/backend_config.py`, `06_05_operator/operator_demo_runner.py`, `06_06_integration/integration_runner.py`, `06_07_polish/demo_runner.py`, `06_08_ui/ui_demo_stack.py`.
- The backend is explicitly dev-memory only: `06_engineering/06_04_backend/backend_storage.py:27-91`, `06_engineering/06_04_backend/backend_app.py:25-35`.
- Evidence is not robustly repeatable. The integration runner assumes exclusive control of fixed broker port `18884` and hard-fails on collision: `06_engineering/06_06_integration/integration_runner.py:161-162`.
- Security posture is almost nonexistent by design: anonymous broker auth is enabled in multiple runners, e.g. `06_engineering/06_03_transport/mqtt_transport_runner.py:61-71`, `06_engineering/06_06_integration/integration_runner.py:99-107`.

## 6. What Is Not Yet Proven
- That the software MVP is ready for real board binding with low integration friction.
- That the operator UI gives a trustworthy end-user interpretation of command acceptance/rejection.
- That the degraded behavior is sufficient for hardware phase, especially for prolonged disconnect behavior.
- That the documented V1 state machine is the real implemented state machine.
- That the evidence chain is truly repeatable on a clean machine without manual cleanup, port hygiene, or hidden local state.

## 7. Engineering Honesty Assessment
Score: 3/5

Strengths:
- The project repeatedly states that hardware-specific code is deferred.
- The stage reports do not pretend to have real AGV proof.
- The repo clearly separates software-only MVP from hardware phase planning.

Weaknesses:
- The contract still advertises states/events not meaningfully implemented in the software path, especially around `MAINTENANCE` and other transition vocabulary. See `06_engineering/06_00_contract/STATE_MACHINE.md` vs. `06_engineering/06_01_sim_twin/twin_models.py:20-38`, `06_engineering/06_01_sim_twin/twin_state_machine.py:10-38`, and `06_engineering/06_02_edge/edge_models.py:8-17`.
- The UI polish claims clearer accepted vs rejected outcomes, but the actual correlation logic is wrong. `use-dashboard.ts` matches event `corr_id` to the UI-generated `corrId` (`06_engineering/06_08_ui/src/hooks/use-dashboard.ts:72-104`), while transport maps edge audit correlation to the command `msg_id`, not that UI `corr_id` (`06_engineering/06_03_transport/mqtt_transport_runner.py:267-293`). This breaks the main operator feedback loop.
- Stage evidence is written largely by the same layer that generates the behavior. There is little independent verification beyond self-run scripts.

Issues:
- Fatal: operator outcome reporting in UI is not trustworthy because correlation logic is inconsistent with actual transport semantics.
- Serious: contract scope and implemented scope are not fully aligned.
- Moderate: evidence claims overstate repeatability relative to the fixed-port reality.
- Low: several reports read more conclusive than the actual runtime maturity justifies.

Must-fix-before-hardware? YES
Must-fix-before-defense? YES

## 8. Architecture Assessment
Score: 2/5

Strengths:
- Boundary intent is good: contract -> edge -> transport -> backend -> operator/UI.
- Hardware abstraction is explicitly reserved for a future adapter boundary.
- UI does not directly bypass backend into MQTT.

Weaknesses:
- Edge runtime is still parasitic on the twin domain through runtime dynamic loading instead of a clean shared package: `06_engineering/06_02_edge/edge_runtime.py:14-38`.
- The twin state machine still mixes transition logic and publish side effects: `06_engineering/06_01_sim_twin/twin_state_machine.py:41-124`.
- Runtime composition across stages depends on ad hoc module loading and `sys.modules` reuse, not stable packaging.
- Integration and operator evidence paths rely on `TestClient` and embedded broker orchestration rather than one clean deployable application topology: `06_engineering/06_05_operator/operator_demo_runner.py:121-180`, `06_engineering/06_06_integration/integration_runner.py:165-176`.

Issues:
- Fatal: none.
- Serious: architecture is still held together by demo scaffolding rather than stable runtime packaging.
- Serious: shared domain logic is not cleanly extracted from simulation-first implementation.
- Moderate: side-effectful state machine will become painful during hardware binding and fault handling extension.
- Low: repo-level organization is better than runtime-level architecture.

Must-fix-before-hardware? YES
Must-fix-before-defense? YES

## 9. Evidence Assessment
Score: 2/5

Strengths:
- There is real evidence, not screenshots-only theater.
- Stage 2 scenarios passed during this audit.
- Edge demo passed during this audit.
- UI build passed during this audit.

Weaknesses:
- Fresh full-chain revalidation failed during this audit because the integration runner assumes exclusive ownership of fixed broker port `18884`.
- Evidence is mostly generated by local runners with embedded broker + in-process app layers. That is useful, but weak as independent proof.
- The project itself already admits prior port conflicts in Stage 7B. That means repeatability is not robust; it is conditional.

Issues:
- Fatal: no fatal evidence fraud detected.
- Serious: current integration evidence is fragile and not clean-room repeatable.
- Serious: UI claim of accepted/rejected outcome clarity is undermined by wrong correlation logic.
- Moderate: there is no independent browser-level verification of what a human actually sees.
- Low: textual reporting quality is high, but that is not the same as strong evidence.

Must-fix-before-hardware? YES
Must-fix-before-defense? YES

## 10. UX / Operator Assessment
Score: 2/5

Strengths:
- The UI is calmer and more understandable than a typical student dashboard.
- It separates status, controls, history, telemetry, and live updates in a readable way.
- Raw JSON is pushed into secondary debug surfaces, which is correct.

Weaknesses:
- The main “latest command outcome” block is not trustworthy because event correlation is wrong: `06_engineering/06_08_ui/src/hooks/use-dashboard.ts:72-104` vs `06_engineering/06_03_transport/mqtt_transport_runner.py:267-293`.
- The UI exposes `UNSUPPORTED_MODE` as a first-class selectable mode in the operator control itself: `06_engineering/06_08_ui/src/components/control-panel.tsx:47-55`. That is acceptable for engineering demo diagnostics, but weak for an operator-facing contour.
- Manual command inputs have no UI-side range discipline and backend validation is weak: `06_engineering/06_04_backend/backend_models.py:50-59`.

Issues:
- Fatal: broken command outcome correlation.
- Serious: operator-facing control still leaks test/demo semantics into the main surface.
- Moderate: input validation is not strong enough for a pre-hardware operator path.
- Low: bilingual/dev terminology remnants are minor compared to the functional issue above.

Must-fix-before-hardware? YES
Must-fix-before-defense? YES

## 11. Safety / Reliability Assessment
Score: 1/5

Strengths:
- The design intent is correct: local safety is supposed to dominate cloud/backend logic.
- Manual commands are rejected outside `MANUAL`: `06_engineering/06_02_edge/edge_runtime.py:220-228`.
- Disconnect degradation exists and removes traction authority.

Weaknesses:
- The contract says disconnect in motion-capable states should go to `DISCONNECTED_DEGRADED` and then `SAFE_STOP` if uncertainty persists (`06_engineering/06_00_contract/MQTT_CONTRACT.md`, heartbeat policy), but the executable supervisor only detects one loss event and then stops progressing: `06_engineering/06_02_edge/edge_heartbeat.py:18-25`.
- Backend control input validation is weak. `requested_mode` is any non-empty string, `linear` and `angular` are unconstrained floats: `06_engineering/06_04_backend/backend_models.py:45-59`.
- MQTT runners use anonymous auth and plaintext local assumptions.
- There is no serious fault-injection, persistence, replay protection, or operator timeout handling beyond minimal contract-level logic.

Issues:
- Fatal: disconnect/degraded behavior is not strong enough yet to be treated as a convincing pre-hardware safety contour.
- Serious: control/API validation is too weak for upcoming board binding.
- Serious: security posture is demo-only.
- Moderate: no durable persistence for command/event history.
- Low: local MVP can tolerate some of this, but defense-grade claims cannot.

Must-fix-before-hardware? YES
Must-fix-before-defense? YES

## 12. Diploma Assessment
Score: 3/5

Strengths:
- The project already exceeds a trivial diploma because it has layered software, a contract, transport, backend, UI, and validation scaffolding.
- The stage-based execution discipline is better than average.
- The project topic is academically defendable if claims stay bounded.

Weaknesses:
- The strongest-looking parts are documents and orchestration, not yet hard proof of a robust control contour.
- The architecture is not elegant enough yet for a “strong” rating.
- The evidence story is not yet hard enough to survive an aggressive examiner.

Issues:
- Fatal: none.
- Serious: mismatch between claimed controller richness and implemented controller depth.
- Serious: evidence repeatability is too fragile for a confident pre-hardware verdict.
- Moderate: UI/operator contour is better-looking than it is trustworthy.
- Low: freeze package is useful but not impressive by itself.

Must-fix-before-hardware? YES
Must-fix-before-defense? YES

## 13. Mandatory Fixes Before Hardware Phase
- Fix command outcome correlation in UI/operator path. The UI must track the real command `msg_id` to the resulting audit event, not a separate UI-generated `corr_id`.
- Reconcile contract and implementation. Either implement the claimed state/event subset or explicitly de-scope what is not in the MVP. No more silent gap between `STATE_MACHINE.md` and executable runtime.
- Hard-stop the evidence fragility. The integration/demo runners need deterministic startup rules, port conflict handling, and a clean reproducible path.
- Strengthen control validation before hardware. Enforce allowed modes and bounded motion ranges at backend/API boundary, not only later in edge logic.
- Define and implement the exact degraded-behavior rule for prolonged link loss. Current one-shot `DISCONNECTED_DEGRADED` handling is not enough.

## 14. Mandatory Fixes Before Final Defense
- Produce one clean independent evidence package where the full chain is re-run from a clean start without hidden occupied ports.
- Remove or isolate demo/test-only controls from the main operator path, especially `UNSUPPORTED_MODE`.
- Replace or drastically reduce dynamic import scaffolding in the runtime path.
- Present a clean “implemented vs deferred vs planned” matrix and keep all thesis claims inside that boundary.
- Add at least one explicit negative validation matrix: illegal mode, illegal reset, bad motion bounds, disconnect, reconnect, stale operator expectation.

## 15. Nice-to-Have Improvements
- Add browser-level smoke automation for key UI states.
- Add persistent backend storage for evidence capture, even if lightweight.
- Add structured scenario traces export instead of console-heavy logs.
- Add formal config files for ports, hosts, retention, timeouts, and demo values.
- Reduce the amount of self-generated reporting language and increase direct machine-verifiable artifacts.

## 16. What Must NOT Be Claimed
- “The system is hardware-ready.”
- “The operator UI reliably confirms accepted and rejected commands.”
- “The implemented controller fully matches the documented V1 state machine.”
- “The software has proven industrial safety.”
- “The backend is PostgreSQL-based in practice.”
- “The transport/integration evidence is robustly repeatable in any local environment.”
- “Orange Pi portability is demonstrated.”
- “Board binding risk is low.”

## 17. Hardware Readiness Gate
NO

Rationale:
- The project is close to being a legitimate pre-hardware software package, but not there yet.
- There is no hardware-specific fraud, which is good.
- The blocker is not missing GPIO code. The blocker is weaker than that and more dangerous: the current software-only proof is not internally tight enough.
- Architecture, evidence, and safety posture still contain issues that will contaminate the hardware phase with ambiguity.

Exact closure conditions for YES:
- UI/operator outcome path is fixed and shown working end-to-end with real accepted/rejected correlation.
- Contract docs are reduced to the actually implemented MVP or implementation is expanded to match the claimed subset.
- One clean full-chain rerun is produced from a clean start without port-collision fragility.
- Backend/API validation is tightened for mode and motion commands.
- Prolonged disconnect behavior is explicitly defined and verified, not just initial degrade transition.
- The project can honestly say: “software-only MVP behavior is proven, operator observation path is trustworthy, and hardware adapter binding is the next bounded step.”

## 18. Top Growth Plan
1. Stop lying to yourselves with ambiguous scope. Align contract, code, and defense wording to one executable MVP.
2. Repair the operator trust loop first. If command outcome reporting is wrong, the human-facing contour is weak by definition.
3. Harden repeatability. One-command clean startup and one-command clean evidence capture matter more now than more features.
4. Tighten control validation and degraded behavior semantics before touching hardware.
5. Strip demo scaffolding out of the runtime path so hardware binding lands on a stable architecture, not a pile of stage runners.

## 19. Final Rating
Acceptable software-only diploma prototype, but not a strong software-only diploma prototype ready for hardware phase.
