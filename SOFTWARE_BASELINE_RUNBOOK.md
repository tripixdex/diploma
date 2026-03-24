# Software Baseline Runbook

## Canonical Baseline
- The canonical full software-only baseline is:
  - `python3 06_engineering/06_08_ui/ui_demo_stack.py`
- This baseline is authoritative because it assembles the local broker-backed edge + backend runtime that the human UI uses.
- This is the reviewer-safe baseline because it exposes the system in the same software-only contour that a supervisor or reviewer can inspect manually.

## Canonical Verification Path
- The canonical health and verification path is:
  - `python3 06_engineering/06_06_integration/integration_runner.py`
- Use it to prove that the software-only chain is healthy without opening the browser UI.

## Start From Scratch
1. Prepare Python from the repo root:
   - `python3.11 -m venv .venv`
   - `source .venv/bin/activate`
   - `python -m pip install --upgrade pip`
   - `python -m pip install -e .`
2. Prepare UI dependencies:
   - `cd 06_engineering/06_08_ui`
   - `npm install`
   - `cd ../..`

## Start The Canonical Baseline
1. Start the software-only runtime stack:
   - `python3 06_engineering/06_08_ui/ui_demo_stack.py`
2. In a second terminal start the UI:
   - `cd 06_engineering/06_08_ui`
   - `npm run dev -- --host 127.0.0.1 --port 5173`
3. Open:
   - `http://127.0.0.1:5173`

## Verify It Is Healthy
- Browser/UI surface:
  - the page loads at `http://127.0.0.1:5173`
- Backend health:
  - `curl -sS http://127.0.0.1:8011/health`
  - expected signal: JSON with `status` equal to `ok`
- Runtime startup output from `ui_demo_stack.py`:
  - `ui_demo_stack_started`
  - `backend=http://127.0.0.1:8011`
  - `ws=ws://127.0.0.1:8011/ws/live`
- Integration verification:
  - `python3 06_engineering/06_06_integration/integration_runner.py`
  - expected signal: final line with `summary: passed=10 total=10`

## Stop The Baseline
- In the terminal that runs `ui_demo_stack.py`, press `Ctrl+C`.
- Stop the Vite UI process with `Ctrl+C`.

## Supporting Paths Only
- `python3 06_engineering/06_07_polish/demo_runner.py`
  - supporting demo wrapper only
  - not the canonical baseline
- `python3 06_engineering/06_04_backend/backend_demo_runner.py`
  - backend-local proof path only
- `python3 06_engineering/06_05_operator/operator_demo_runner.py`
  - operator-path proof path only
- `python3 06_engineering/06_03_transport/mqtt_transport_runner.py`
  - transport proof path only

## Explicitly Not Part Of This Baseline
- Hardware-specific code
- GPIO / Raspberry Pi / Orange Pi binding
- Real AGV wiring or safety validation
- Docker deployment
- PostgreSQL runtime path
- Deployment-grade Mosquitto proof
- Webots
