# Stage 7D Human UI

This directory contains a demo-grade human UI for the frozen software-only MVP.

It provides:
- a React + Vite operator console;
- a minimal shadcn/ui-style component layer;
- REST + WebSocket integration against the existing backend path;
- a local demo stack runner that keeps broker, edge gateway, and backend available for the UI.

It does not provide:
- hardware-specific code;
- Raspberry Pi or Orange Pi binding;
- Webots integration;
- a heavy enterprise frontend stack.

## Manual Run
1. Start the software-only demo stack:
   - `python3 06_engineering/06_08_ui/ui_demo_stack.py`
2. In a second terminal install UI dependencies:
   - `cd 06_engineering/06_08_ui && npm install`
3. Start the Vite UI:
   - `npm run dev -- --host 127.0.0.1 --port 5173`
4. Open:
   - `http://127.0.0.1:5173`
5. Optional smoke validation:
   - `node ui_smoke.mjs`

## Demo Path
- system status is read from backend REST;
- recent events, commands, and telemetry are read from backend REST;
- live updates are consumed from backend WebSocket;
- mode/manual/reset commands are sent through backend REST, which publishes to the existing MQTT contract path.
