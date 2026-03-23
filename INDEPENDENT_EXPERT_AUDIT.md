# Independent Expert Audit

## 1. Audit Scope
Evaluated:
- current repository snapshot as of 2026-03-23;
- software-only MVP contour in `06_engineering/06_00_contract/` through `06_engineering/06_08_ui/`;
- execution reports in `99_reports/execution/`;
- operator/UI/demo/integration evidence;
- current readiness for entering the first hardware-binding phase.

Intentionally not evaluated:
- real AGV hardware behavior;
- electrical compatibility, wiring, signal integrity, and safety chain implementation;
- Raspberry Pi or Orange Pi real deployment behavior;
- physical motion quality, timing, EMC, thermal behavior, and lab-side operational constraints.

Important scope note:
- the user framed the audit around Stages 0-7D.1;
- the repository snapshot itself already contains Stage 7F corrective artifacts and the master report marks Stage 7F as active;
- this audit therefore evaluates the actual repository state, not only the user framing.

## 2. Executive Verdict
This is not a fake project and not an empty mockup. A real software-only contour exists and runs end-to-end.

It is still not honest enough, not clean enough, and not evidence-hard enough to justify a clean transition to hardware phase. The core problem is no longer "nothing works". The core problem is "too much is claimed at the top level relative to what is actually frozen and evidenced, while the engineering base remains demo-fragile."

## 3. Scorecard
| Block | Score | Short verdict |
| --- | --- | --- |
| Engineering honesty | 3/5 | Better than average, but still contaminated by inflated top-level claims. |
| Architecture quality | 3/5 | Layering is real; execution model is still script-heavy and brittle. |
| Hardcode / config discipline | 3/5 | Acceptable for demo; not tight enough for lab binding. |
| Modularity / maintainability | 2/5 | Separated by folders, but not yet engineered as a maintainable runtime product. |
| Evidence quality | 2/5 | Repeatable demo evidence exists, but proof quality is still too self-referential. |
| UX / operator clarity | 3/5 | Good enough for demo and manual checking; not rigorously validated. |
| Security / safety posture | 2/5 | Safety intent exists, but trust boundary and access model are weak and demo-local only. |
| Diploma strength | 3/5 | Acceptable software prototype, not yet a strong diploma-grade software package. |

## 4. What Is Actually Strong
- The project has a real bounded software contour: contract, twin, edge logic, MQTT transport, backend, operator path, integration runner, and browser UI.
- The system is not pretending cloud/server state is the safety authority. Edge-side state logic remains the primary decision point.
- Deferred scope is often stated honestly inside stage reports and freeze documents.
- The Stage 7F fixes addressed a real weakness: command dispatch is no longer falsely presented as command acceptance.
- The UI is not just decorative. It is attached to the backend path, exposes command outcome semantics, and is usable for manual operator-path checking.
- The integration runner is real evidence. During this audit it passed end-to-end with `10/10 PASS`.

## 5. What Is Weak or Fragile
- Top-level source-of-truth documents still overstate the implemented stack and stage outcomes.
- The Python runtime is held together by repeated dynamic module loading and script runners instead of a clean package/runtime structure.
- Evidence is mostly self-generated markdown plus demo script output; it is not yet a disciplined verification package.
- Deployment readiness is weak: no Python environment manifest, no service definition, no serious hardware-phase runtime packaging.
- Security posture is effectively "trusted local demo only", but that constraint is not elevated strongly enough as a hard boundary.
- Stage gate discipline is partially undermined by stale or inflated gate wording.

## 6. What Is Not Yet Proven
- Webots-based simulation environment.
- PostgreSQL-backed backend persistence.
- Docker Compose deployment.
- Mosquitto-based broker deployment.
- Raspberry Pi 4 binding behavior.
- Any real AGV I/O mapping.
- Any hardware-valid emergency-stop integration.
- Any real-time or quasi-real-time timing behavior on target hardware.
- Any production-grade security or operator authorization model.
- Any long-run stability beyond short scripted runs.

## 7. Engineering Honesty Assessment

### Engineering honesty
- Score: 3/5
- Strengths:
  - Stage reports repeatedly state that the project is software-only and that hardware-specific work is deferred.
  - Stage 5 report honestly admits that PostgreSQL is not implemented.
  - Stage 2 report honestly admits that the twin is not a Webots scene.
  - Stage 7F narrows the contract toward the actually implemented MVP subset.
- Weaknesses:
  - `SYSTEM_SCOPE.md` still presents `PostgreSQL`, `Docker Compose`, and `Webots` as part of the V1 working result and core stack.
  - `MASTER_EXECUTION_REPORT.md` still says Stage 2 prepares a Webots environment and Stage 5 evidences a FastAPI + PostgreSQL backend path.
  - The repo simultaneously contains honest local corrections and inflated top-level summaries. That split is dangerous for defense.
- Fatal issues:
  - Source-of-truth inflation at the top level. If the committee reads top-level docs first, they get a stronger project than the repo actually proves.
- Serious issues:
  - Gate wording and actual implementation evidence are not fully reconciled.
  - "Independent expert audit" is referenced in the master report while root-level audit artifacts were not the obvious primary source in the repo root at audit time.
- Moderate issues:
  - Some cross-stage language still reflects roadmap ambition rather than frozen MVP reality.
- Low issues:
  - Minor terminology drift between stage names and what the stage actually delivered.
- Must-fix-before-hardware? YES
- Must-fix-before-defense? YES

## 8. Architecture Assessment

### Architecture quality
- Score: 3/5
- Strengths:
  - The contour is correctly layered: contract -> twin -> edge -> transport -> backend -> operator/UI.
  - HardwareAdapter abstraction is defined before hardware binding.
  - Edge state machine remains the core authority.
  - Degraded behavior is modeled explicitly and is now better aligned with evidence.
- Weaknesses:
  - Runtime composition depends heavily on ad hoc script orchestration and dynamic import loaders.
  - The same broker/bootstrap patterns are duplicated across multiple runners.
  - Architecture is more "demo harness architecture" than "pre-hardware runtime architecture".
- Fatal issues:
  - None.
- Serious issues:
  - The project is not packaged as a coherent Python application; it is a collection of cooperating stage scripts.
  - There is no credible deployment/runtime assembly for the first board-binding iteration.
- Moderate issues:
  - Repeated embedded broker implementations and repeated import-loader scaffolding create maintenance drag.
  - Transport/demo/backend integration is overly tied to local script startup patterns.
- Low issues:
  - Some docs still describe future architecture more strongly than current code deserves.
- Must-fix-before-hardware? YES
- Must-fix-before-defense? YES

### Hardcode / config discipline
- Score: 3/5
- Strengths:
  - MQTT port is overrideable through env and Stage 7F added port fallback in key paths.
  - Command ranges and reset allowlists are now explicitly validated.
  - Topic names are centralized rather than sprayed through the codebase.
- Weaknesses:
  - Important runtime values are still hardcoded in multiple places: ports, client IDs, timeouts, demo values, local URLs.
  - Config discipline is sufficient for localhost demo, not for first lab deployment.
  - Browser/backend coordination still assumes a fixed local topology.
- Fatal issues:
  - None.
- Serious issues:
  - Configuration is not yet organized as a pre-hardware deployment matrix.
- Moderate issues:
  - UI timeout constants are embedded in code.
  - Multiple local defaults remain implicit rather than explicitly stage-scoped.
- Low issues:
  - Demo-preferred values are exposed in UI text rather than centralized config.
- Must-fix-before-hardware? YES
- Must-fix-before-defense? YES

### Modularity / maintainability
- Score: 2/5
- Strengths:
  - Domain areas are physically separated into stage folders.
  - Backend validation logic and transport contracts are isolated reasonably well.
- Weaknesses:
  - There is no proper Python package/application structure for the whole runtime.
  - I found no real automated Python test suite under `06_engineering`.
  - Dynamic import patterns are repeated across transport, operator, integration, polish, and UI stack runners.
  - Maintenance burden will rise sharply once hardware binding starts.
- Fatal issues:
  - None.
- Serious issues:
  - Lack of a test suite means every change remains "rerun scripts and hope".
  - Runtime assembly logic is duplicated instead of shared.
- Moderate issues:
  - Backend, transport, and operator harnesses are closer to scenario demos than reusable services.
- Low issues:
  - Naming is mostly clean, but the repository still leans heavily on stage-oriented rather than product-oriented organization.
- Must-fix-before-hardware? YES
- Must-fix-before-defense? YES

## 9. Evidence Assessment

### Evidence quality
- Score: 2/5
- Strengths:
  - Real runnable evidence exists.
  - During this audit:
    - `python3 06_engineering/06_06_integration/integration_runner.py` passed with `summary: passed=10 total=10`;
    - `python3 -m py_compile ...` passed for the software contour;
    - `npm run build` passed for the UI.
  - Stage reports usually state what was and was not validated.
- Weaknesses:
  - Evidence is still mostly self-produced textual reporting plus console runs, not a hardened verification package.
  - Stage gate docs and master summary still contradict lower-level honest reports.
  - Screenshot/browser proof is still manual.
  - No long-run soak, restart robustness, fault injection depth, or environment-lock proof exists.
- Fatal issues:
  - The evidence chain is partially undermined by source-of-truth documents that overclaim Webots/PostgreSQL-level readiness.
- Serious issues:
  - No formal automated test suite.
  - No stable exported evidence pack with preserved logs/artifacts per gate.
  - No Python dependency manifest means reproducibility depends too much on the current machine state.
- Moderate issues:
  - UI evidence is good enough for demo but not strong enough for a harsh review board.
- Low issues:
  - Lack of screenshot automation.
- Must-fix-before-hardware? YES
- Must-fix-before-defense? YES

## 10. UX / Operator Assessment

### UX / operator clarity
- Score: 3/5
- Strengths:
  - The UI now distinguishes `отправлено` from `принято`/`отклонено` correctly.
  - Operator flow is step-based and human-readable.
  - Russian-first presentation is mostly consistent.
  - The screen is actually useful for manual checking during a software-only demo.
- Weaknesses:
  - Validation is still mostly developer-performed manual QA.
  - There is no real operator study, no error-rate evidence, and no usability measurement.
  - Some engineering terms remain visible because the UI still doubles as a debugging surface.
- Fatal issues:
  - None.
- Serious issues:
  - None.
- Moderate issues:
  - UX proof is weaker than the UX itself.
  - It remains a demo operator surface, not a validated HMI.
- Low issues:
  - No browser-level visual regression harness.
- Must-fix-before-hardware? NO
- Must-fix-before-defense? NO

## 11. Safety / Reliability Assessment

### Security / safety posture
- Score: 2/5
- Strengths:
  - Local safety intent is clear: uncertainty should collapse to degraded or stop states.
  - Command validation is materially better after Stage 7F.
  - Prolonged disconnect escalation to `SAFE_STOP` is now implemented and evidenced.
- Weaknesses:
  - MQTT broker is anonymous in the demo contour.
  - REST and WebSocket paths have no authentication or authorization.
  - Safety remains software-semantic only; there is still no hardware trust boundary.
  - Reset/recovery semantics are not yet tied to real interlock conditions.
- Fatal issues:
  - None inside software-only scope, provided nobody lies about safety validation.
- Serious issues:
  - The operational trust model is only acceptable for a trusted localhost demo environment.
  - There is no explicit pre-hardware operating policy that constrains where this insecure contour may be used.
- Moderate issues:
  - No rate limiting, no session model, no command authorization, no hardened broker identity model.
  - Reliability proof is short-run only.
- Low issues:
  - UI health indicators are informative, not operationally authoritative.
- Must-fix-before-hardware? YES
- Must-fix-before-defense? YES

## 12. Diploma Assessment

### Diploma strength
- Score: 3/5
- Strengths:
  - This is beyond a toy mockup. There is a legitimate software system here.
  - The repo shows disciplined stage thinking, contract thinking, and evidence intent.
  - The project already has enough substance to become a strong diploma.
- Weaknesses:
  - Right now it is easier to defend as "acceptable software prototype" than as "strong engineering-ready pre-hardware package".
  - The strongest weakness is not missing features. It is mismatch between ambitious umbrella wording and narrower proven reality.
  - A tough commission can attack the project on proof rigor and implementation maturity before they attack it on scope.
- Fatal issues:
  - None.
- Serious issues:
  - Without claim cleanup and evidence hardening, the diploma story becomes vulnerable to accusations of overstatement.
- Moderate issues:
  - Missing packaging, deployment, and reproducibility discipline reduce perceived engineering maturity.
- Low issues:
  - The UI helps, but does not by itself lift the work into a strong diploma tier.
- Must-fix-before-hardware? YES
- Must-fix-before-defense? YES

## 13. Mandatory Fixes Before Hardware Phase
- Rewrite top-level source-of-truth documents so they describe the actual current MVP, not the planned stack. `Webots`, `PostgreSQL`, `Docker Compose`, and `Mosquitto` must move from implied-current to explicitly deferred unless directly evidenced.
- Reconcile `SYSTEM_SCOPE.md`, `STAGE_GATE_CRITERIA.md`, and `MASTER_EXECUTION_REPORT.md` with the actual current repository state.
- Produce one clean reproducible Python environment entrypoint: dependency manifest plus one documented command path for full-chain verification.
- Reduce script fragility: shared runtime/bootstrap utilities instead of repeated dynamic loader and embedded broker boilerplate.
- Freeze a pre-hardware operational policy:
  - local trusted network only;
  - no security claims;
  - no safety claims beyond software semantics;
  - explicit no-motion/no-energize rules until board survey is complete.
- Export a real evidence pack for the current gate:
  - command truth-loop proof;
  - invalid-command rejection;
  - degraded to safe-stop escalation;
  - backend validation rejection;
  - UI operator flow proof;
  - retained logs, not only narrative markdown.

## 14. Mandatory Fixes Before Final Defense
- Keep all hardware-phase claims tightly bounded by actual evidence collected later.
- Add real automated tests for the core state machine, validation layer, and at least one full integration smoke path.
- Convert the software contour from script collection into a cleaner package/runtime structure.
- Add reproducible deployment/runtime documentation for the target board path once hardware binding starts.
- Preserve a defense-safe evidence index with exact commands, outputs, and resulting artifacts.
- Clean the diploma narrative so the committee cannot catch obvious stack inflation in the first five minutes.

## 15. Nice-to-Have Improvements
- Screenshot-based UI regression proof.
- Simple service supervision templates for the later board path.
- Persistent backend storage once it becomes relevant to the defended scope.
- Limited operator role model if the project later claims anything beyond trusted local demo use.
- A concise architecture diagram set aligned exactly to the implemented MVP subset.

## 16. What Must NOT Be Claimed
- "Webots simulation environment is implemented and evidenced."
- "PostgreSQL backend is implemented."
- "Docker Compose deployment exists."
- "Mosquitto-based deployment is validated."
- "The system is hardware-ready."
- "Raspberry Pi binding is already prepared beyond abstraction and planning."
- "Emergency-stop behavior is validated on the robot."
- "Safety is proven."
- "The system is production-secure."
- "The UI is a validated industrial HMI."
- "Long-run reliability is proven."
- "The project is already an industrial-grade cloud-edge AGV system."

## 17. Hardware Readiness Gate
- NO

Rationale:
- A real software-only MVP exists. That part is no longer the blocker.
- The blocker is that the project still has unresolved fatal honesty/evidence problems at the source-of-truth layer and serious pre-hardware engineering weaknesses at the runtime/deployment layer.
- Hardware phase should not start from a repo where top-level documents still imply stronger stack readiness than the code proves.
- Hardware phase should not start from a contour that is reproducible mainly through local script choreography without a clean runtime package and environment baseline.
- The UI/operator path is already good enough for manual checking in the lab.
- The board-binding preparation concept exists.
- The project is close, but not yet clean enough to say: "now go to the university lab and bind hardware honestly."

Exact closure conditions for YES:
- `SYSTEM_SCOPE.md`, `STAGE_GATE_CRITERIA.md`, and `MASTER_EXECUTION_REPORT.md` are rewritten to match actual implemented reality.
- One reproducible environment setup exists for the Python contour.
- One clean full-chain verification path exists without loader duplication and without relying on fragile ad hoc orchestration.
- A retained evidence pack exists for the current software-only gate.
- The project explicitly constrains current safety/security claims to trusted local software-only lab use.
- Pre-hardware entry docs clearly define what will be measured in the first lab trip and what remains forbidden to claim.

## 18. Top Growth Plan
1. Kill inflated claims first. This is the highest-leverage correction because it improves honesty, defense safety, and hardware-gate credibility immediately.
2. Stabilize runtime assembly. Replace duplicated bootstrap code and dynamic-import glue with a shared package-level startup path.
3. Lock reproducibility. Add Python environment manifest and one authoritative runbook for the full software contour.
4. Harden evidence. Save logs/artifacts from the exact scenarios that justify the gate.
5. Enter hardware phase only after the software package is modest, clean, reproducible, and impossible to accuse of bluffing.

## 19. Final Rating
Acceptable software-only diploma prototype.

Not yet a strong software-only diploma prototype ready for hardware phase.
