# Independent Expert Re-Run

## 1. Re-Run Scope
This re-run evaluates the project after Stage 7F as a software-only MVP package before hardware phase. It does not evaluate real hardware behavior, GPIO binding, electrical safety, motor drivers, real sensor semantics, or lab deployment. It does evaluate whether the Stage 7E blocker set was actually closed and whether the current software package is honest enough to justify opening hardware phase.

Re-run spot checks performed on 2026-03-23:
- `python3 -m py_compile 06_engineering/06_01_sim_twin/*.py 06_engineering/06_02_edge/*.py 06_engineering/06_03_transport/*.py 06_engineering/06_04_backend/*.py 06_engineering/06_06_integration/*.py 06_engineering/06_08_ui/ui_demo_stack.py` -> passed.
- `npm run build` in `06_engineering/06_08_ui` -> passed.
- `python3 06_engineering/06_06_integration/integration_runner.py` -> passed `10/10`; broker selected fallback port because `18884` was occupied and the rerun still completed.

## 2. Executive Verdict
The mandatory Stage 7E blockers are now materially closed. The project is no longer blocked by an untrustworthy UI truth loop, an overstated contract, or a fragile fixed-port rerun path.

That does not make the project elegant. It is still demo-heavy, architecture is still scaffold-driven, backend posture is still dev-grade, and the operator surface still leaks test semantics into the main flow. So the honest verdict is narrow:

- Hardware Readiness Gate can now be lifted.
- Strong software-only diploma prototype rating still cannot be granted.

This is now an acceptable pre-hardware software package, not a strong one.

## 3. Scorecard
| Block | Score | Short verdict | Issues | Must-fix-before-hardware? | Must-fix-before-defense? |
| --- | --- | --- | --- | --- | --- |
| Engineering honesty | 4/5 | The project is now mostly honest about what is implemented and what is deferred. | Serious: deferred scope still lives in code-level enums and long-term docs; Moderate: some reports still sound more mature than the runtime really is. | NO | YES |
| Architecture quality | 2/5 | Functional layering exists, but runtime composition is still held together by dynamic loader scaffolding and demo orchestration. | Serious: pervasive `importlib` runtime loading; Serious: simulation-first state machine still drives non-simulation runtime; Moderate: packaging is still weak. | NO | YES |
| Hardcode / configuration discipline | 3/5 | Better than Stage 7E because the critical rerun path no longer dies on a fixed MQTT port. | Serious: many defaults remain localhost/demo-centric; Moderate: fallback hardening is concentrated in Stage 7 paths, not all legacy runners. | NO | YES |
| Modularity / maintainability | 2/5 | The repository is tidy, but the executable system is still too stage-runner-centric. | Serious: shared runtime logic is still coupled to demo code paths; Moderate: maintainability will degrade as hardware adapters appear unless packaging is cleaned up. | NO | YES |
| Evidence quality | 3/5 | Evidence is now reproducible enough to justify the gate, but still mostly self-generated. | Serious: little independent verification beyond local runners; Moderate: browser-level operator proof is still weak. | NO | YES |
| UX / operator clarity | 3/5 | The operator path is now materially more trustworthy and Russian-first on the main surface. | Serious: the main control still exposes `UNSUPPORTED_MODE`; Moderate: inputs remain engineering-demo oriented rather than operator-disciplined. | NO | YES |
| Security / safety posture | 2/5 | The safety story is acceptable only as software-only pre-hardware scaffolding. | Serious: anonymous plaintext local MQTT; Serious: backend still has no auth and no durable evidence chain; Moderate: safety semantics remain software-only, not hardware-proven. | NO | YES |
| Diploma strength | 3/5 | Defensible diploma material exists, but the software package is still not strong enough to impress a hard examiner. | Serious: architecture remains inelegant; Serious: proof remains more convincing than before but still not rigorous enough for a strong rating. | NO | YES |

## 4. Previously Identified Blockers: Closed or Not?
### UI truth loop
Closed.

Reason:
- Backend publish receipt now returns command `msg_id`.
- UI tracks that `msg_id` and waits for `event/audit` tied to that command instead of treating dispatch as success.
- The current implementation now distinguishes `published` from `accepted/rejected`.

Residual risk:
- If audit never arrives, the UI can only show timeout / non-authoritative status. That is acceptable for this stage.

### Contract / implementation reconciliation
Closed.

Reason:
- Contract documents now explicitly limit the active MVP subset.
- `MAINTENANCE` is marked as deferred instead of being quietly presented as implemented.
- Disconnect escalation semantics are described in the narrowed contract and now match runtime behavior.

Residual risk:
- The codebase still contains deferred enum vocabulary. That is not fraud anymore, but it remains a cleanliness debt.

### Rerun fragility
Closed for the blocker scope.

Reason:
- The critical full-chain rerun path now rebinds to a free MQTT port if `18884` is occupied.
- This re-run verified that exact case in practice: integration completed on a fallback port and still passed `10/10`.

Residual risk:
- Not every legacy standalone runner received the same level of hardening.

### Backend / API validation hardening
Closed.

Reason:
- `requested_mode` is allowlisted.
- manual numeric ranges are bounded.
- reset action/state pairing is validated before publish.
- invalid requests are rejected at backend boundary.

Residual risk:
- This is validation hardening, not security hardening.

### Prolonged disconnect behavior
Closed.

Reason:
- The runtime now has explicit two-step behavior: `heartbeat_lost -> DISCONNECTED_DEGRADED`, then `prolonged_disconnect -> SAFE_STOP`.
- The re-run integration scenario exercised and passed that chain.

Residual risk:
- Thresholds remain software-only values with no hardware timing proof.

### Russian-first UI consistency
Closed.

Reason:
- Main operator-facing UI language is now Russian-first.
- Technical tokens remain only where they are contract identifiers and are still understandable in context.

Residual risk:
- The control surface still includes engineering-test semantics that weaken operator purity more than language consistency.

Bottom line: the six mandatory blocker groups from Stage 7E are closed.

## 5. What Is Actually Strong Now
- The project is materially more honest than it was at Stage 7E.
- The full software chain is real and re-runnable.
- The exact Stage 7E fixed-port failure mode has been neutralized in the critical rerun path.
- The operator truth loop is now credible enough for software-only proof.
- Disconnect handling is no longer a one-shot degrade gesture; it now has a defined escalation path.
- The thesis can now defend a bounded claim set without obvious internal contradiction.

## 6. What Is Still Weak or Fragile
- The architecture is still not clean. Dynamic runtime module loading remains everywhere it should not be.
- The backend remains dev-grade: in-memory, local-first, unauthenticated.
- Evidence is still mostly generated by project-owned scripts rather than by independent test harnesses.
- The operator UI still mixes demonstration and operator concerns by exposing unsupported-mode testing in the main control path.
- The project remains stronger in staged orchestration and documentation than in runtime elegance.

## 7. What Is Not Yet Proven
- That board binding will be low-friction.
- That timing assumptions for disconnect and recovery thresholds survive real hardware noise.
- That the operator UX is robust under real load, repeated runs, or fault storms.
- That the backend/event chain is suitable for anything beyond local demo and validation.
- That the software architecture will remain manageable once hardware-specific adapters are added.

## 8. Engineering Honesty Assessment
Score: 4/5

Verdict:
The project is now substantially more honest than before. The most dangerous Stage 7E honesty gaps were the fake truth loop and the inflated contract. Those were corrected.

Fatal issues:
- None.

Serious issues:
- Deferred concepts still remain visible in code structure and long-term language, which can invite overclaiming if the defense wording gets sloppy.

Moderate issues:
- Some reporting language still sounds cleaner and more mature than the runtime warrants.

Low issues:
- None worth blocking the gate.

Must-fix-before-hardware? NO
Must-fix-before-defense? YES

## 9. Architecture Assessment
Score: 2/5

Verdict:
The project works. The architecture is still inelegant.

Fatal issues:
- None.

Serious issues:
- Runtime composition still depends on dynamic module loading instead of stable packaging.
- The system remains stage-runner-centric instead of product-runtime-centric.

Moderate issues:
- Shared domain logic is still simulation-shaped and will likely accumulate pain during hardware binding.

Low issues:
- Repository organization is better than runtime architecture.

Must-fix-before-hardware? NO
Must-fix-before-defense? YES

## 10. Evidence Assessment
Score: 3/5

Verdict:
Evidence quality is no longer blocker-grade weak. It is now acceptable, not strong.

Fatal issues:
- None.

Serious issues:
- Evidence remains mostly self-produced by local integrated runners.
- There is still limited independent proof of what the operator actually sees.

Moderate issues:
- The rerun path is hardened where it mattered, but reproducibility quality is still uneven across the repo.

Low issues:
- Textual reporting remains better than raw machine-verifiable artifact depth.

Must-fix-before-hardware? NO
Must-fix-before-defense? YES

## 11. UX / Operator Assessment
Score: 3/5

Verdict:
The UI is now trustworthy enough for a bounded software-only operator proof. It is still not a clean operator-grade surface.

Fatal issues:
- None.

Serious issues:
- The main control panel still exposes `UNSUPPORTED_MODE` as a first-class selectable action. That belongs in diagnostics, not in the default operator workflow.

Moderate issues:
- Manual input UX is still demo-oriented and weakly disciplined from an HMI perspective.

Low issues:
- Remaining English technical tokens are acceptable because they map to contract identifiers.

Must-fix-before-hardware? NO
Must-fix-before-defense? YES

## 12. Safety / Reliability Assessment
Score: 2/5

Verdict:
The project now clears the specific pre-hardware software gate. It does not clear any serious operational safety claim.

Fatal issues:
- None within the honest software-only stage boundary.

Serious issues:
- MQTT and backend posture remain open, local, and demo-grade.
- No claim of industrial or deployment-grade reliability can be defended.

Moderate issues:
- Disconnect semantics are now defined, but hardware-realistic timing and failure modes remain unproven.

Low issues:
- None.

Must-fix-before-hardware? NO
Must-fix-before-defense? YES

## 13. Diploma Assessment
Score: 3/5

Verdict:
This is now a defensible diploma-stage software prototype. It is still not a strong one.

Fatal issues:
- None.

Serious issues:
- The architecture is too improvised to earn a strong mark from a hard technical examiner.
- The evidence story is acceptable, not impressive.

Moderate issues:
- The project still relies heavily on stage discipline and documentation to carry perceived maturity.

Low issues:
- None.

Must-fix-before-hardware? NO
Must-fix-before-defense? YES

## 14. Mandatory Fixes Before Hardware Phase
None from the Stage 7E blocker set remain mandatory.

Conditions attached to that statement:
- Hardware phase may open only as an honestly bounded next step.
- The project must not reinterpret this as proof of hardware readiness in operation.
- The project must preserve the corrected contract boundary and not re-expand claims without implementation.

## 15. Mandatory Fixes Before Final Defense
- Remove or isolate `UNSUPPORTED_MODE` and other test semantics from the main operator flow.
- Reduce dynamic import scaffolding in the runtime path and present a cleaner architectural story.
- Produce a cleaner implemented / deferred / future matrix and keep defense wording inside it.
- Strengthen evidence independence: at minimum one more defense-grade proof package with direct machine-verifiable artifacts and less narrative padding.
- Prepare a hard limitations slide/page that explicitly states what is still software-only and what is not proven.

## 16. Nice-to-Have Improvements
- Add browser-level smoke checks for key operator flows.
- Add persistent lightweight storage for evidence retention instead of purely in-memory traces.
- Separate operator mode from diagnostic/test mode in the UI.
- Move runtime composition away from ad hoc dynamic loading toward one stable package layout.
- Add a compact negative-test matrix for command rejection, disconnect, reset misuse, and timeout handling.

## 17. What Must NOT Be Claimed
- “The system is operationally safe.”
- “The system is deployment-ready.”
- “The architecture is production-grade.”
- “The backend is hardened.”
- “The hardware integration risk is low.”
- “The operator interface is already industrial HMI quality.”
- “Real AGV behavior has been validated.”
- “This is a strong software-only prototype” without major qualification.

## 18. Hardware Readiness Gate
YES

Rationale:
- The six blocker groups that previously justified `Hardware Readiness Gate = NO` are now closed in code, contract, and rerun evidence.
- The exact Stage 7E rerun fragility was re-tested and no longer blocks the chain.
- The software-only MVP is now internally honest enough to serve as a bounded base for hardware integration work.

This YES is narrow:
- It means the project may proceed into hardware phase preparation.
- It does not mean the system is hardware-validated.
- It does not mean the project is strong.

## 19. Final Rating
The project is now an acceptable software-only diploma prototype that is ready to enter hardware phase.

It is still not a strong software-only diploma prototype. The blockers were closed; the underlying architecture and rigor were not transformed into excellence.
