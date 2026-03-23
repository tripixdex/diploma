# UI State Model

## Primary Slices
- `health`: backend availability and command bridge readiness.
- `currentStatus`: latest backend status snapshot.
- `recentEvents`: latest event/alarm/audit records.
- `recentCommands`: latest command records observed by backend.
- `recentTelemetry`: latest telemetry snapshots.
- `liveFrames`: rolling list of WebSocket updates.
- `lastDispatch`: most recent REST command dispatch receipt or failure.
- `wsState`: `connecting`, `live`, or `idle`.

## Update Sources
- Initial load: REST snapshot.
- Ongoing updates: WebSocket live feed plus periodic REST refresh.
- Command actions: REST POST responses followed by backend-observed MQTT evidence.

## UI Truth Rules
- status, events, commands, and telemetry are rendered from backend data, not local guesses;
- command success is only a publish receipt, not a hidden business success claim;
- command rejection is shown through audit/event evidence from the backend feed;
- missing data is shown honestly as unavailable, not fabricated.
