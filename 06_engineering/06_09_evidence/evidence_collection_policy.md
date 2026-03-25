# Evidence Collection Policy

## Principles
- Save real artifacts, not reconstructed stories.
- Keep artifacts compact and reviewer-usable.
- Separate software-only proof from deferred or absent proof.
- If a proof artifact is missing, say so explicitly.

## Provenance Minimums
- Every primary reviewer-facing artifact should have a run-stamped filename.
- Every mandatory scenario should have its exact run path recorded in `scenario_to_artifact_matrix.md`.
- Expected outcome and actual outcome must be written separately, not implied.
- Failure signature must be explicit enough that a reviewer can tell what would count as a bad run.
- If an artifact predates provenance tightening and lacks a run stamp, keep it only in `artifacts/legacy_pre_7F63/` and do not present it as the preferred baseline.

## Included Artifact Types
- Compact runner console logs.
- Compact health/HTTP outputs.
- Compact smoke summaries.
- Short UI proof summaries tied to exact commands and saved outputs.
- Cross-links to frozen truth/freeze documents where the artifact is a document rather than a runtime log.

## Excluded Artifact Types
- Giant raw dumps.
- Full broker traces.
- Fabricated screenshots.
- Hardware or deployment claims without direct evidence.
- Browser automation frameworks added only for evidence cosmetics.

## Evidence Honesty Rules
- `PASS` means the artifact exists and supports the scenario directly.
- `FAIL` means the scenario was attempted and did not meet expectation.
- `PARTIAL` should be used if only some sub-claims are evidenced.
- Missing screenshots or other non-critical artifacts must be stated as missing rather than implied.
- A document cross-link may support a scope-boundary claim, but it does not replace runtime proof for runtime behavior.

## Failure Interpretation
- A proof artifact is good enough when it contains a direct success signature that matches the matrix expectation.
- A proof artifact is not good enough if success must be inferred from silence or from unrelated lines.
- If a failure signature is present, the scenario must not remain marked `PASS`.

## Software-Only Boundary
This pack does not prove:
- hardware readiness,
- GPIO integration,
- Raspberry Pi or Orange Pi binding,
- Docker deployment,
- PostgreSQL runtime,
- Webots integration,
- real AGV safety behavior.
