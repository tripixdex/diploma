# Software-Only Evidence Pack

This directory is the reviewer-facing evidence pack for the current AGV Denford software-only MVP.

It is intentionally narrow:
- compact real artifacts,
- strict scenario-to-artifact provenance,
- explicit software-only limits,
- no hardware or deployment bluffing.

Start here:
- `evidence_index.md`
- `scenario_to_artifact_matrix.md`
- `software_only_claims_evidence_map.md`

Primary reviewer-safe artifacts are now grouped by purpose:
- `artifacts/logs/`
- `artifacts/http_ws/`
- `artifacts/summaries/`
- `artifacts/ui/`

Legacy flat artifacts collected before provenance tightening are retained only for traceability:
- `artifacts/legacy_pre_7F63/`

The current reviewer-facing baseline should use the run-stamped artifacts in the purpose-specific subfolders, not the legacy flat files.
