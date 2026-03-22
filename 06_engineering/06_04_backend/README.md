# Backend MVP

Stage 5 adds a minimal backend path for AGV Denford without UI and without hardware-specific code.

What it does:
- ingests real MQTT messages through a Paho-based bridge;
- stores command, event, status, and telemetry data in a dev/demo storage path;
- exposes a minimal FastAPI REST API;
- exposes a minimal WebSocket live feed.

What it does not do:
- it does not implement UI;
- it does not integrate with real GPIO or Raspberry Pi hardware;
- it does not provide production PostgreSQL deployment in this stage.

This stage reuses the Stage 1 contract and Stage 4 transport topic/payload rules. The current storage path is PostgreSQL-ready by interface, but the demo implementation remains explicitly dev-only.
