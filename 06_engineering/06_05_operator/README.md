# Operator Path MVP

Stage 6 adds a minimal operator-facing path for AGV Denford without introducing a heavy UI stack.

What it does:
- reads current status, recent events, and recent telemetry from the Stage 5 backend;
- subscribes to backend live updates through WebSocket;
- publishes minimal operator commands through the existing MQTT contract path;
- demonstrates a lightweight CLI-style operator console flow.

What it does not do:
- it does not implement a full web UI;
- it does not add hardware-specific code;
- it does not replace backend, transport, or edge responsibilities.

This stage reuses the existing Stage 1 contract, Stage 4 transport topics/payloads, and Stage 5 backend API/WebSocket path.
