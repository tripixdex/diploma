# UI Architecture

The Stage 7D UI is a thin human-facing layer over the frozen software-only MVP.

## Boundaries
- `ui_demo_stack.py`: local runtime helper that keeps the demo contour alive for the browser UI.
- React app: renders the operator-facing surface.
- `src/lib/api.ts`: REST boundary for status, history, telemetry, and command dispatch.
- `src/hooks/use-dashboard.ts`: local state orchestration and live update integration.
- `src/components/ui/*`: minimal shadcn/ui-style primitives.

## Data Flow
1. Browser fetches current status, recent events, recent commands, and recent telemetry from the Stage 5 backend.
2. Browser opens a WebSocket to `/ws/live`.
3. Browser sends control actions through backend REST command endpoints.
4. Backend publishes the command into the existing MQTT path.
5. Edge reacts and publishes audit/status/telemetry/alarm evidence.
6. Backend stores and broadcasts those updates.
7. UI refreshes lists and live panel without introducing a new protocol.

## UI Responsibilities
- make state, mode, and alerts immediately readable;
- provide minimal safe controls;
- surface rejected command feedback honestly;
- remain small, calm, and demo-grade.

## Non-Responsibilities
- business logic duplication from backend or edge;
- transport logic reimplementation;
- board-specific runtime behavior;
- heavy frontend productization.
