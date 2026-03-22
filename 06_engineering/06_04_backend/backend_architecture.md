# Backend Architecture

## Stage Purpose
Stage 5 introduces the first backend contour between MQTT transport and future operator/backend services. It remains backend-only and does not include UI or hardware integration.

## Module Boundaries
- `backend_config.py`: backend runtime settings and shared transport/topic imports.
- `backend_models.py`: typed backend records and API-facing payload models.
- `backend_storage.py`: storage boundary and current in-memory dev/demo implementation.
- `backend_mqtt_bridge.py`: real MQTT ingest layer using Paho and the Stage 4 topic contract.
- `backend_api.py`: REST endpoints over backend storage.
- `backend_ws.py`: live stream hub and WebSocket endpoint.
- `backend_app.py`: FastAPI assembly and backend context wiring.
- `backend_demo_runner.py`: local demo that proves MQTT ingest, storage, REST, and WebSocket behavior.

## Data Flow
1. MQTT producer publishes contract-compatible messages.
2. `BackendMqttBridge` subscribes to command and state/event topics.
3. Incoming payloads are decoded and normalized into backend records.
4. Storage updates:
   - command log
   - event/alarm/audit log
   - latest status snapshot
   - telemetry snapshots
5. Live stream hub broadcasts the normalized record to WebSocket subscribers.
6. REST API exposes stored backend state.

## Storage Strategy
- Target path: PostgreSQL-ready storage abstraction.
- Current Stage 5 path: `InMemoryBackendStorage`, explicitly marked as dev/demo only.
- This keeps the backend runnable without crossing into Stage 6 deployment/UI work.

## Why This Still Fits Stage 5
- MQTT ingest is real.
- API and WebSocket are real backend boundaries.
- No UI, no hardware access, no Docker full stack, and no Webots integration are added here.
