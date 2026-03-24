# Stage 07F.2 Report

## Stage ID and name
- Stage ID: Sprint 7F.2
- Stage name: Packaging / Reproducibility Cleanup

## Objective
- Introduce one honest, modern, reproducible packaging and setup baseline for the current software-only MVP without changing runtime behavior or scope.

## Input context used
- `README.md`
- `TOP_LEVEL_TRUTH_BASELINE.md`
- `06_engineering/06_06_integration/release_manifest.md`
- `06_engineering/06_08_ui/README.md`
- Active Python runtime entrypoints in `06_engineering/`
- Existing UI `package.json`

## Files created
- `pyproject.toml`
- `SOFTWARE_RUNTIME_BASELINE.md`
- `99_reports/execution/STAGE_07F2_REPORT.md`

## Files updated
- `README.md`
- `TOP_LEVEL_TRUTH_BASELINE.md`
- `06_engineering/06_06_integration/release_manifest.md`
- `06_engineering/06_08_ui/README.md`
- `99_reports/execution/MASTER_EXECUTION_REPORT.md`

## Packaging baseline summary
- Added `pyproject.toml` as the authoritative Python metadata and dependency baseline.
- Python dependency truth is no longer implicit across scattered files and local memory.
- `pyproject.toml` is intentionally minimal and honest: it defines metadata, Python version range, and runtime dependencies without pretending the repo is already a polished PyPI/distribution package.

## Reproducibility summary
- Added a single top-level runtime baseline document that explains Python setup, UI setup, and canonical run flow from scratch.
- Python setup and UI setup are now explicitly separated.
- Canonical full-chain reviewer path and non-UI evidence path are both documented.

## Canonical setup/run path summary
- Python:
  - create `.venv`
  - `python -m pip install -e .`
- UI:
  - `cd 06_engineering/06_08_ui && npm install`
- Full-chain demo:
  - `python3 06_engineering/06_08_ui/ui_demo_stack.py`
  - `cd 06_engineering/06_08_ui && npm run dev -- --host 127.0.0.1 --port 5173`
- Non-UI repeatable evidence:
  - `python3 06_engineering/06_06_integration/integration_runner.py`

## Remaining reproducibility risks
- This sprint does not provide Docker Compose or one-command full-stack packaging.
- This sprint does not provide PostgreSQL packaging or migration baseline.
- Local environment still needs Python and Node installed manually.
- Pre-existing repo clutter such as `.DS_Store` files still exists outside this sprint scope.

## Validation performed
- Verified that `pyproject.toml` exists and is parseable as the canonical Python metadata file.
- Verified that Python dependency truth is explicit in `pyproject.toml`.
- Verified that canonical setup/run documentation exists in `SOFTWARE_RUNTIME_BASELINE.md`.
- Verified that UI setup path is documented clearly in `SOFTWARE_RUNTIME_BASELINE.md` and `06_engineering/06_08_ui/README.md`.
- Verified that top-level docs now point to the runtime baseline.
- Verified that no new hardware or deployment-grade claims were introduced.
- Verified that runtime behavior was not expanded beyond packaging/reproducibility scope.

## READY TO CLOSE?
- YES

## Reasoned recommendation
- Close Sprint 7F.2 after this packaging/reproducibility baseline correction.
- Do not move into runtime/bootstrap cleanup or evidence-pack work automatically.
- Use `pyproject.toml` plus `SOFTWARE_RUNTIME_BASELINE.md` as the new reviewer-facing setup truth until the next corrective sprint is explicitly opened.

## Sanitation check
- No repo clutter was introduced by Sprint 7F.2.
- All changed files remain in correct folders.
- File names remain understandable.
- No temp/random files were created by this sprint.
- No runtime behavior was expanded beyond packaging/reproducibility scope.
- Top-level docs remain honest about the software-only contour.
- Pre-existing `.DS_Store` files remain in the repository outside this sprint scope.

## Prompt re-check

### Required
- Introduce a Python packaging baseline with `pyproject.toml`.
- Make Python dependency truth explicit.
- Clarify UI dependency/install path.
- Create one canonical software-only setup/run path.
- Create `SOFTWARE_RUNTIME_BASELINE.md`.
- Update top-level entry docs as needed.
- Create/update `STAGE_07F2_REPORT.md`.
- Update `MASTER_EXECUTION_REPORT.md` for Sprint 7F.2.
- Perform sanitation check.
- Perform required/done/not done/why re-check.
- Validate packaging and documentation coherence.

### Done
- `pyproject.toml` was added.
- Python version range and dependencies were made explicit.
- UI install/dev/build path was documented clearly.
- `SOFTWARE_RUNTIME_BASELINE.md` was created as the canonical setup/run truth artifact.
- Top-level docs were updated to point to the new runtime baseline.
- `MASTER_EXECUTION_REPORT.md` was aligned to Sprint 7F.2.

### Not done
- No bootstrap/runtime refactor.
- No new evidence pack.
- No packaging as a deployment-grade product.
- No hardware-specific work.
- No repo-wide cleanup of pre-existing `.DS_Store` files.

### Why
- These items are explicitly outside Sprint 7F.2 scope.
- The sprint goal is packaging/reproducibility hygiene, not runtime redesign or deployment expansion.
