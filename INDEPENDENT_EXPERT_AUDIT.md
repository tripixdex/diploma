# Independent Expert Audit

## 1. Audit Scope

This audit evaluates the repository strictly as a `software-only MVP + UI + demo + freeze package` for the AGV Denford diploma project.

Assessed:
- system contract and scope discipline;
- software architecture across twin, edge, transport, backend, operator/UI, evidence layers;
- configuration and hardcode discipline;
- maintainability and modularity;
- quality of evidence and repeatability claims;
- operator-facing clarity and diagnostic usefulness;
- software-side safety posture and degraded behavior logic;
- diploma strength at the current software-only stage.

Explicitly not assessed as implemented proof:
- Raspberry Pi or Orange Pi binding;
- GPIO, motor driver, sensor wiring, or power path behavior;
- real AGV safety on hardware;
- deployment-grade packaging;
- Webots implementation;
- PostgreSQL runtime implementation.

## 2. Executive Verdict

The project is not fake. That already puts it above a large fraction of diploma repositories.

But it is still a bounded software demonstration, not a robust engineering platform. The strongest part is not technical depth; it is unusually strict claim control and a real end-to-end local contour that currently runs. The weakest part is that too much of the proof is runner-driven, demo-shaped, in-memory, unauthenticated, and weakly tested. This is acceptable for a pre-hardware software stage. It is not strong enough to bluff maturity, deployment readiness, or serious validation depth.

## 3. Scorecard

| Block | Score | Short verdict |
| --- | --- | --- |
| Engineering honesty | 4.5/5 | Surprisingly disciplined; claims are narrower than the usual diploma fiction. |
| Architecture quality | 3.5/5 | Layering is real, but held together by dynamic loader glue and demo-oriented assembly. |
| Hardcode / config discipline | 3.0/5 | Better than a hackathon repo, still too many baked-in demo assumptions. |
| Modularity / maintainability | 3.5/5 | Boundaries exist, but package structure and runtime composition remain awkward. |
| Evidence quality | 3.5/5 | Real artifacts and a passing full-chain runner exist, but the evidence is narrow and mostly self-generated. |
| UX / operator clarity | 4.0/5 | Operator flow is understandable and honest about dispatch vs acceptance. |
| Security / safety posture | 2.5/5 | Local degraded behavior exists, but security is intentionally weak and safety is only software-contract level. |
| Diploma strength | 4.0/5 | Strong software-only diploma stage if presented honestly; weak if oversold. |

## 4. What Is Actually Strong

- The repository explicitly distinguishes implemented truth from roadmap fiction in top-level baselines, claim maps, and policy files.
- The software-only end-to-end contour is real and currently rerunnable: `operator -> backend -> MQTT -> edge -> MQTT -> backend -> operator`.
- The edge logic is not just a UI mock. It has a real state machine, command rejection, heartbeat supervision, degraded behavior, and escalation to `SAFE_STOP`.
- The UI does not lie about command success. Dispatch and acceptance are separated through the audit path.
- Evidence is organized as a pack, not scattered screenshots and vague prose.
- The project is prepared for hardware abstraction conceptually: edge logic does not directly depend on GPIO calls.

## 5. What Is Weak or Fragile

- The project relies heavily on custom runtime bootstrapping and dynamic module loading because the codebase is not packaged coherently.
- The proof is still demo-shaped. The integration runner assembles a friendly local world and then proves that friendly local world.
- Storage is in-memory only. This is acceptable now, but it sharply limits claims about durability, diagnostics, and operational realism.
- Security is almost nonexistent by design: anonymous broker, open CORS for local origins, no auth on control APIs, no operator identity, no audit attribution beyond message IDs.
- There is effectively no real automated test suite. There are test plans and runners, not serious regression coverage.
- Some configuration is still frozen around local ports, local hostnames, demo timings, and local dev assumptions.
- The UI is good enough for demonstration, not yet strong as an operator console under stress, noise, or fault-heavy scenarios.

## 6. What Is Not Yet Proven

- Any real board support.
- Any real AGV interface support.
- Any real safety behavior on hardware.
- Any deployment-grade runtime.
- Any persistence-grade backend path.
- Any portability to Orange Pi.
- Any Webots implementation.
- Any security or multi-user operational model.
- Any timing realism beyond local developer-machine execution.

## 7. Engineering Honesty Assessment

### Verdict

This is the strongest dimension of the project.

The repo repeatedly states that it proves only a software-only MVP, explicitly defers hardware, PostgreSQL, Webots, Docker, Mosquitto deployment, and forbids those claims in policy. That is rare and correct.

### Strengths

- Top-level documents are aligned with current implementation truth, not wishlist language.
- Deferred items are named explicitly instead of being left vague.
- Hardware readiness is kept blocked in policy rather than implied.
- Evidence mapping clearly separates `EVIDENCED` from `DEFERRED / MUST NOT CLAIM`.

### Weaknesses

- The repo still contains a lot of stage/roadmap/process language. That creates a nonzero risk that a reviewer will mistake closure paperwork for technical maturity.
- Some artifacts are self-authored summaries rather than independent measurements.
- The project is honest in documents, but a sloppy oral defense could still overclaim if the student loses discipline.

### Issues

- Fatal: none found.
- Serious: evidence is still mostly self-generated and local; honesty is strong, but proof depth is still limited.
- Moderate: closure/status language can create an illusion of stronger maturity than the code itself deserves.
- Low: some long-term architecture wording still exceeds the implemented subset.

### Must Fix Flags

- Must fix before hardware: `NO`
- Must fix before defense: `YES`

Reason:
- Not because honesty is bad now, but because defense language must be locked down even harder than repository language.

## 8. Architecture Assessment

### Verdict

The architecture is legitimate, not theatrical. But it is still an MVP architecture, not a clean, production-caliber platform.

### Layer-by-layer assessment

#### Contract layer

Strong.
- The contract is bounded and materially reflected in the software subset.
- State model and command philosophy are coherent.

Weak.
- Deferred concepts like broader V1 ambition still remain near the active subset, which invites future drift.

#### Twin / domain layer

Reasonable.
- A state machine exists and drives actual behavior.
- Illegal transitions and manual-command safety rejection are explicit.

Weak.
- The twin still carries deferred `MAINTENANCE` state in enums even though the MVP does not implement it.
- Contract logic is still relatively thin. It is enough for MVP proof, not enough for claims of rich operational behavior.

#### Edge layer

Useful, but demo-oriented.
- Edge runtime performs local validation and heartbeat escalation.
- Separation via adapter boundary is correct.

Weak.
- Edge runtime dynamically imports domain modules from stage folders through `sys.modules` tricks instead of normal package composition.
- Safety semantics are software-level only and timing thresholds are arbitrary demo constants.

#### Transport layer

Adequate for current scope.
- Real MQTT exchange exists.

Weak.
- Embedded anonymous broker is acceptable for demo, but it is not a serious transport posture.
- Message handling remains simple and trust-heavy.

#### Backend layer

Good enough for a diploma MVP.
- REST, WebSocket, ingest, and command publishing are present.
- Validation of mode/manual/reset is visibly tighter than a naive pass-through backend.

Weak.
- In-memory storage only.
- No identity, auth, authorization, persistence, or replay strategy.
- Backend start-up assumes ideal local conditions.

#### UI / operator layer

Better than expected for a diploma MVP.
- Main scenario is human-readable.
- The command truth loop is handled correctly.

Weak.
- It remains a narrow single-screen demo console, not a robust operator workstation.

### Strengths

- Real layer separation exists.
- Edge remains the authority, not the backend.
- Adapter boundary protects later board binding from immediate contamination.

### Weaknesses

- Dynamic loading is an architectural smell and a maintainability tax.
- The runtime is assembled from stage folders rather than from a stable application package.
- Several components are coupled through shared naming and loader behavior rather than explicit package contracts.

### Issues

- Fatal: none found.
- Serious: architecture still depends on dynamic bootstrap glue instead of a normal package/application assembly.
- Moderate: too much of the runtime remains optimized for demo orchestration instead of stable long-term composition.
- Low: enum and contract remnants of deferred states/features can cause drift.

### Must Fix Flags

- Must fix before hardware: `YES`
- Must fix before defense: `YES`

Reason:
- Hardware phase will become harder, not easier, if board-specific code is added on top of loader-driven glue.

## 9. Evidence Assessment

### Verdict

Evidence is real, organized, and better than average. It is still narrower than the project may be tempted to imply.

### Strengths

- There is a structured evidence layer with artifact mapping.
- The integration runner currently passes end-to-end and proves a real contour.
- The repo distinguishes evidence for current software-only truth from absent evidence for deferred topics.

### Weaknesses

- Most evidence is generated by project-owned scripts in project-owned conditions.
- Evidence depth is shallow: one canonical contour, limited scenario diversity, limited fault injection diversity, limited persistence and recovery proof.
- There is no strong automated regression suite behind the evidence pack.
- `ui_smoke` is environment-sensitive and not a substitute for actual browser-level verification.

### Issues

- Fatal: none found.
- Serious: evidence breadth is too narrow to support big claims beyond the frozen software-only contour.
- Moderate: artifacts are summary-heavy and could use stronger provenance, timestamps, and rerun discipline.
- Low: some evidence files are almost ceremonial and add little beyond what runner logs already prove.

### Must Fix Flags

- Must fix before hardware: `YES`
- Must fix before defense: `YES`

Reason:
- Before hardware, the current software baseline must be rock-solid and reproducible.
- Before defense, evidence needs a cleaner, harder reviewer-facing narrative than “the script passed on my machine.”

## 10. UX / Operator Assessment

### Verdict

This is a competent demo UI, not a cosmetic decoy. It helps the operator understand what the system thinks is happening. That matters.

### Strengths

- Russian-first wording is appropriate for the target defense/demo context.
- Flow is staged and understandable.
- UI explicitly explains that `отправлено` is not equal to `принято`.
- Status, recent events, commands, telemetry, and live frames are visible in one surface.
- Unsupported mode can be triggered deliberately to demonstrate rejection behavior.

### Weaknesses

- The UI still assumes a calm demo environment and a trained presenter.
- It is more of a validation console than a true operator HMI.
- There is little prioritization, escalation, filtering, or operational focus for fault-heavy situations.
- It depends on understanding contract tokens like `MANUAL`, `AUTO_LINE`, `SAFE_STOP`.

### Issues

- Fatal: none found.
- Serious: none at current software-only stage.
- Moderate: operator assistance is limited once the scenario deviates from the expected demo path.
- Low: some mixed technical vocabulary remains visible and acceptable only because this is still a technical MVP.

### Must Fix Flags

- Must fix before hardware: `NO`
- Must fix before defense: `NO`

Reason:
- The UI is already adequate for demonstrating and manually checking the current MVP.

## 11. Safety / Reliability Assessment

### Verdict

There is real software-side safety intent, but no one should confuse that with validated system safety.

### Strengths

- Edge authority is local.
- Link loss moves the system to `DISCONNECTED_DEGRADED` and then to `SAFE_STOP`.
- Illegal commands are rejected.
- Emergency stop and fault concepts are explicitly above normal mode commands in the contract.
- The repo repeatedly forbids claims of real hardware safety proof.

### Weaknesses

- Safety is only software-contract level today.
- Timing thresholds are arbitrary and not tied to measured platform behavior.
- There is no demonstrated watchdog, process supervision, persistence of critical fault history, or recovery hardening.
- The transport and backend security model is too weak for any serious operational context.
- Anonymous MQTT and unauthenticated control endpoints are acceptable only inside a tightly controlled local demo.

### Issues

- Fatal: none found, because the repo does not claim real AGV safety proof.
- Serious: unauthenticated command/control path and anonymous broker mean the current contour is operationally unsafe outside a trusted local demo.
- Moderate: degraded behavior is proven only in one local software contour, not under broader failure modes.
- Low: some safety semantics still rely on implied rather than measured timing assumptions.

### Must Fix Flags

- Must fix before hardware: `YES`
- Must fix before defense: `YES`

Reason:
- Before hardware, the pre-hardware safety boundary must be even more explicit and operationally enforced.
- Before defense, the student must not accidentally describe these mechanisms as validated safety.

## 12. Diploma Assessment

### Verdict

At the current stage, this is a strong software-only diploma prototype if and only if it is defended honestly as a software-only prototype.

It becomes a weak diploma instantly if presented as “AGV modernization already implemented,” “hardware-ready,” or “safety-proven.”

### Strengths

- The project is structured, bounded, and technically coherent.
- It has actual software layers instead of one script and a fake UI.
- It has reviewable artifacts, policies, and a real end-to-end contour.
- It shows engineering discipline, not just coding activity.

### Weaknesses

- There is no deep algorithmic novelty yet.
- There is no real hardware validation yet.
- There is little evidence of performance characterization, fault coverage, or deployment maturity.
- Too much of the project’s apparent mass comes from documentation and stage governance rather than deeper technical depth.

### Issues

- Fatal: none found.
- Serious: the diploma becomes intellectually weak if the narrative overweights process closure and underweights technical limitations.
- Moderate: current novelty is more in disciplined system packaging than in control/intelligence sophistication.
- Low: the repo can appear bureaucratically oversized relative to the actual implemented software core.

### Must Fix Flags

- Must fix before hardware: `NO`
- Must fix before defense: `YES`

Reason:
- The defense story must sell the right thing: an honestly frozen software-only architecture and proof baseline for later hardware integration.

## 13. Mandatory Fixes Before Hardware Phase

- Remove architecture fragility from the runtime assembly path.
  Meaning: stop relying so heavily on dynamic stage-folder loading and `sys.modules` composition for canonical runtime paths.
- Freeze one canonical, reviewer-safe software baseline with hard rerun instructions and one-command verification.
  Meaning: the same baseline that will be used before every lab session must be reproducible, boring, and deterministic.
- Strengthen evidence provenance.
  Meaning: artifact timestamps, rerun procedure, exact commands, expected outcomes, and failure signatures must be explicit.
- Tighten pre-hardware operational safety boundaries.
  Meaning: trusted-local-only assumptions, no-open-network rule, allowed lab actions, forbidden energization/motion actions, and recovery limits must be explicit and non-negotiable.
- Produce a first hardware-survey-ready package.
  Meaning: contract subset, I/O assumptions, checklist, photo plan, signal questions, and board-binding placeholders must be concise enough to carry into the lab without interpretation drift.

## 14. Mandatory Fixes Before Final Defense

- Lock presentation language so no deferred item can be accidentally spoken as implemented.
- Produce a cleaner evidence narrative for reviewers.
  Meaning: what was run, what passed, what exactly it proves, and what it absolutely does not prove.
- Add at least a minimal real automated regression suite for critical software behaviors.
  Minimum acceptable scope: contract transitions, command rejection, heartbeat degradation, backend validation.
- Reduce demo-only architectural smell.
  If full repackaging is too expensive, at least isolate and explain the dynamic loader assembly as technical debt, not as “architecture.”
- State security and safety limitations bluntly in the defense package.

## 15. Nice-to-Have Improvements

- Replace in-memory storage with a modest persistence-backed path after hardware phase starts.
- Add browser-level UI smoke verification instead of relying mainly on API/WebSocket checks.
- Add richer fault injection scenarios.
- Add more operator guidance for off-nominal states.
- Add timing and resource measurements on the future target board.

## 16. What Must NOT Be Claimed

- “The project is hardware-ready.”
- “Raspberry Pi 4 support is already implemented.”
- “Orange Pi portability is proven.”
- “Real AGV safety is validated.”
- “The backend is deployment-grade.”
- “The system is production-ready.”
- “PostgreSQL is the current runtime backend.”
- “Docker deployment is implemented and validated.”
- “Mosquitto deployment baseline is proven.”
- “Webots integration is already implemented.”
- “The software has comprehensive automated test coverage.”
- “The operator UI proves real industrial HMI readiness.”

## 17. Hardware Readiness Gate

### NO

### Rationale

The software-only MVP is real enough. That is not the blocker.

The blocker is that the project is ready only for an honest hardware-survey entry, not yet ready for an honest hardware-phase start under a strong gate definition. The missing closure is not “more random coding.” The missing closure is a tighter pre-hardware baseline: stable runtime assembly, stronger evidence provenance, explicit operational safety restrictions, and a physically grounded survey package tied back to the software contract.

If the question is “can the student go to the lab and start surveying hardware facts without lying about the project?”, the answer is close to yes.

If the question is the stricter one required here, “can the project already claim hardware-phase readiness?”, the answer is no.

### Exact closure conditions for YES

- The canonical software-only baseline is rerunnable without fragile setup surprises.
- Critical software behaviors have at least minimal automated regression coverage.
- The runtime assembly debt is either reduced or formally frozen as known technical debt with controlled entrypoints.
- Pre-hardware operating policy is explicit, narrow, and enforceable.
- First-lab survey packet is complete and directly mapped to board/power/ESTOP/I/O unknowns.
- Defense and documentation language is locked against overclaiming.

## 18. Top Growth Plan

1. Harden the software baseline instead of adding features.
2. Replace documentation-heavy confidence with stronger executable regression proof.
3. Simplify runtime composition before contaminating it with board-specific code.
4. Treat the first hardware visit as a survey mission, not an integration mission.
5. Preserve the current honesty discipline at all costs.

## 19. Final Rating

`strong software-only diploma prototype, but not yet honestly ready for hardware phase`

