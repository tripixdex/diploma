# System Contract

## V1 Purpose
V1 is a simulation-first system contract for digital modernization of AGV Denford with an edge + cloud architecture. Its purpose is to define the minimum bounded behavior required for supervised command execution, state control, telemetry delivery, operator visibility, and evidence collection without claiming hardware behavior that is not yet verified.

## Current Software-Only MVP Scope
At the current pre-hardware stage, the implemented and evidenced MVP subset is narrower than the long-term contract ambition:
- Implemented and evidenced now: `INIT`, `IDLE`, `MANUAL`, `AUTO_LINE`, `SAFE_STOP`, `ESTOP_LATCHED`, `FAULT`, `DISCONNECTED_DEGRADED`.
- Implemented operator commands now: `cmd/mode` for `MANUAL` and `AUTO_LINE`, bounded `cmd/manual`, and reset requests that are validated against current state rules.
- Implemented degraded behavior now: `heartbeat_lost -> DISCONNECTED_DEGRADED`, followed by `prolonged_disconnect -> SAFE_STOP` if link loss persists.
- Explicitly deferred from the current MVP: `MAINTENANCE` state and its transitions, board-specific safety wiring, GPIO binding, and any hardware-validated recovery semantics.

## System Boundary
The V1 system boundary includes:
- the onboard control application running on Raspberry Pi class hardware;
- the transport layer based on MQTT;
- the server-side telemetry and operator-facing service boundary;
- the simulation environment used as the first validation target;
- the operator control path for bounded, supervised commands.

The V1 system boundary excludes:
- hardware motor driver details not yet surveyed;
- certified safety systems;
- autonomous navigation beyond bounded line-following logic;
- ROS 2, Gazebo, CV, SLAM, fleet management, and digital twin expansion beyond simulation support.

## External Actors
- Operator: selects mode, issues bounded commands, observes state, acknowledges alarms where applicable.
- Supervisor or lab engineer: configures test environment, reviews logs, validates scenarios.
- Local safety contour: emergency-stop chain and hardware interlocks external to cloud/backend logic.
- MQTT broker: message exchange infrastructure, not a decision-making actor.
- Simulation environment: provides virtual plant and sensor context for Stage 2+ validation.

## Internal Subsystems
- Edge control service: enforces state machine, accepts valid commands, applies safety gating, publishes state.
- HardwareAdapter boundary: isolates GPIO, sensor reads, traction enable, and board-specific details.
- MQTT transport client: exchanges commands, state, telemetry, alarms, heartbeat, and audit events.
- Server/backend boundary: receives telemetry and state, persists records, exposes operator-facing data path.
- Operator-facing boundary: user interface or thin control surface consuming backend/state information.
- Evidence and reporting boundary: logs, reports, scenario traces, and validation artifacts used for VKR proof.

## Operating Modes
- `INIT`: startup checks and initial state publication.
- `IDLE`: motion disabled, waiting for valid command or mode selection.
- `MANUAL`: supervised operator-driven motion commands within bounded limits.
- `AUTO_LINE`: bounded line-following mode under local safety constraints.
- `SAFE_STOP`: commanded or protective controlled stop with motion disabled.
- `ESTOP_LATCHED`: emergency stop latched until local reset conditions are satisfied.
- `FAULT`: internal software or hardware-related fault state requiring explicit operator or maintenance action.
- `DISCONNECTED_DEGRADED`: broker/server link degraded while local safe behavior is preserved.

Deferred beyond the current software-only MVP:
- `MAINTENANCE`: diagnostics/configuration mode with motion path restricted. This state is kept only as a deferred design direction and is not implemented or evidenced yet.

## State Model Overview
V1 uses a single authoritative edge-side state machine. Commands are advisory inputs, not direct actuator authority. Motion-capable states are only `MANUAL` and `AUTO_LINE`. Any uncertainty in safety-critical preconditions must collapse to `SAFE_STOP`, `ESTOP_LATCHED`, or `FAULT` depending on trigger severity. Cloud/server state visibility is informative and must not be treated as the source of truth for safe stop behavior.

## Safety Principles
- Local safe stop behavior must not depend on cloud availability.
- Loss of broker/backend/operator connectivity must not leave traction enabled indefinitely.
- If connectivity loss persists after the initial degraded transition, the current MVP must escalate from `DISCONNECTED_DEGRADED` to `SAFE_STOP`.
- Emergency stop has higher priority than any mode or motion command.
- Illegal state transition requests are rejected and must generate audit/fault evidence.
- V1 must preserve the legacy local safety contour and must not bypass it in software.
- Safety claims are limited to designed behavior at contract level until validated in simulation or hardware.

## Command / Telemetry / Event Philosophy
- Commands are explicit requests with validation, acknowledgement semantics, and rejection reasons.
- State messages represent the current authoritative state of the edge controller.
- Telemetry messages carry periodic operational measurements and context for evidence.
- Event messages capture alarms, faults, audits, and significant transitions.
- Every critical transition must be externally visible through MQTT evidence.
- Payloads must be structured for traceability rather than convenience-driven ad hoc fields.

## Hardware Abstraction Principle
All hardware-specific logic must be hidden behind a `HardwareAdapter` boundary. State logic, command validation, MQTT messaging, and server contracts must operate on logical signals, not on GPIO pin numbers, library-specific calls, or one exact Raspberry Pi revision. The contract remains valid for Raspberry Pi 4 as target hardware and Raspberry Pi Model B+ / 3B+ as fallback hardware.

## Explicit Assumptions
- Exact final Raspberry Pi model is not confirmed.
- V1 is simulation-first and may progress before full hardware survey.
- Local safety contour exists outside cloud/backend logic.
- MQTT is the approved transport baseline for V1.
- FastAPI and PostgreSQL are approved backend technologies for later stages.
- Webots is the approved Stage 2 simulation environment.

## Explicit Non-Assumptions
- V1 does not assume any exact GPIO map yet.
- V1 does not assume verified motor driver interface details.
- V1 does not assume certified safety integrity.
- V1 does not assume continuous cloud connectivity.
- V1 does not assume autonomous route planning or fleet behavior.
- V1 does not assume hardware-realistic timing until measured.
