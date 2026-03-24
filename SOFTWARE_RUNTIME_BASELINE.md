# Software Runtime Baseline

## Supported Environment Assumptions
- This baseline is for the current software-only MVP only.
- Supported host OS is any developer machine that can run Python and Node locally.
- No hardware-specific code, GPIO, Raspberry Pi binding, or Webots setup is part of this baseline.
- No deployment-grade packaging is claimed here.
- Operating policy boundaries are fixed separately in [pre_hardware_operating_policy.md](/Users/vladgurov/Desktop/study/7sem/diploma/06_engineering/06_10_policy/pre_hardware_operating_policy.md).

## Python Version Expectation
- Canonical Python range: `>=3.11,<3.13`
- The repo now uses [pyproject.toml](/Users/vladgurov/Desktop/study/7sem/diploma/pyproject.toml) as the authoritative Python metadata and dependency baseline.

## Python Setup Path
1. Create and activate a virtual environment:
   - `python3.11 -m venv .venv`
   - `source .venv/bin/activate`
2. Upgrade installer basics:
   - `python -m pip install --upgrade pip`
3. Install the Python baseline from the repo root:
   - `python -m pip install -e .`

## UI Setup Path
- The UI lives in `06_engineering/06_08_ui/`.
- Canonical install command:
  - `cd 06_engineering/06_08_ui && npm install`
- Canonical dev command:
  - `npm run dev -- --host 127.0.0.1 --port 5173`
- Canonical build command:
  - `npm run build`
- UI dependency truth stays in `06_engineering/06_08_ui/package.json` and `package-lock.json`.

## Canonical Full-Chain Run Path
This is the canonical reviewer-facing software-only run path:

1. Prepare Python environment from the repo root using `pyproject.toml`.
2. Prepare UI dependencies in `06_engineering/06_08_ui/` with `npm install`.
3. Start the software-only stack:
   - `python3 06_engineering/06_08_ui/ui_demo_stack.py`
4. In a second terminal start the UI:
   - `cd 06_engineering/06_08_ui && npm run dev -- --host 127.0.0.1 --port 5173`
5. Open:
   - `http://127.0.0.1:5173`

## Canonical Non-UI Evidence Path
- For repeatable software-only evidence without the browser UI:
  - `python3 06_engineering/06_06_integration/integration_runner.py`

## Runtime Assembly Baseline
- Canonical software-only entrypoints now share a small bootstrap utility in `06_engineering/runtime_bootstrap.py`.
- This utility centralizes:
  - dynamic module loading that is still needed because active stage directories are not normal Python packages,
  - embedded local broker startup/shutdown,
  - local Uvicorn thread startup/shutdown,
  - broker port fallback selection for the canonical integration and UI demo paths.
- This is a coherence cleanup only. It does not add new business capabilities or deployment claims.

## Demo / Dev Only
- `ui_demo_stack.py` is a local software-only demo stack, not a deployment baseline.
- Embedded/local broker usage is demo/dev infrastructure, not proof of deployment-grade broker packaging.
- Backend storage evidence is still a dev/demo path, not PostgreSQL runtime proof.

## Known Limitations
- No Docker Compose packaging baseline yet.
- No PostgreSQL runtime packaging baseline yet.
- No deployment-grade Mosquitto baseline yet.
- No Webots setup/run path yet.
- No hardware phase bootstrap, board binding, or safety validation.

## What Is Not Yet Packaged / Deployment-Grade
- Full-stack deployment.
- Hardware runtime bootstrap.
- Board-specific service setup.
- Production process supervision.
- Production-ready environment management.
