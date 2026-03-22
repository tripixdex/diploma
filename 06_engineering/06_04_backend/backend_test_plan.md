# Backend Test Plan

## What Stage 5 Must Verify
- backend MQTT ingest receives real MQTT messages over a local broker path;
- command messages are stored;
- event/audit/alarm messages are stored;
- latest status snapshot is updated;
- telemetry snapshots are stored;
- REST API returns stored backend data;
- WebSocket live feed accepts a client and emits live backend records.

## What Stage 5 Does Not Verify
- PostgreSQL production deployment;
- operator UI;
- real Raspberry Pi / GPIO / AGV hardware integration;
- Docker full-stack orchestration;
- Webots integration;
- long-run reliability and production security.

## Minimum Mandatory Demo
1. Start local broker path.
2. Start backend MQTT ingest bridge.
3. Publish at least one command, one audit/event, one status, and one telemetry message.
4. Confirm REST endpoints return persisted data.
5. Confirm WebSocket endpoint accepts a client and receives a live record.
