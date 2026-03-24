# Evidence Collection Policy

## Principles
- Save real artifacts, not reconstructed stories.
- Keep artifacts compact and reviewer-usable.
- Separate software-only proof from deferred or absent proof.
- If a proof artifact is missing, say so explicitly.

## Included Artifact Types
- Compact runner console logs.
- Compact health/HTTP outputs.
- Compact smoke summaries.
- Cross-links to frozen truth/freeze documents where the artifact is a document rather than a runtime log.

## Excluded Artifact Types
- Giant raw dumps.
- Full broker traces.
- Fabricated screenshots.
- Hardware or deployment claims without direct evidence.

## Evidence Honesty Rules
- `PASS` means the artifact exists and supports the scenario directly.
- `FAIL` means the scenario was attempted and did not meet expectation.
- `PARTIAL` should be used if only some sub-claims are evidenced.
- Missing screenshots or other non-critical artifacts must be stated as missing rather than implied.

## Software-Only Boundary
This pack does not prove:
- hardware readiness,
- GPIO integration,
- Raspberry Pi or Orange Pi binding,
- Docker deployment,
- PostgreSQL runtime,
- Webots integration,
- real AGV safety behavior.
