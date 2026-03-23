# System Scope

## V1 Working Result
V1 of the AGV Denford modernization project is a simulation-first, software-only edge + cloud MVP for supervised command exchange, telemetry delivery, operator visibility, and evidence-oriented validation.

## In Scope
- Simulation-first architecture for AGV Denford modernization.
- Edge component boundaries for onboard control integration on Raspberry Pi class hardware.
- MQTT-based transport between edge and server layers.
- Server-side API and telemetry storage boundaries.
- Operator-facing monitoring and control boundary definition.
- Stage-based engineering execution with explicit evidence collection.
- Validation artifacts required to prove implementation incrementally.
- Honest separation between software-only evidence and deferred hardware claims.

## Out of Scope
- ROS 2 in MVP.
- Gazebo in MVP.
- Computer vision, SLAM, autonomous navigation research, or fleet management in MVP.
- Full digital twin overengineering beyond simulation needed for MVP validation.
- Hardware-specific optimization for a single confirmed Raspberry Pi revision at this stage.
- Claims of real hardware functionality before evidence exists.
- Claiming Webots, PostgreSQL, Docker Compose, or production deployment as implemented truth unless separately evidenced.

## Fixed Architectural Principles
- Architecture is edge + cloud.
- Transport baseline is MQTT.
- Current evidenced implementation baseline is Python, local MQTT-backed transport, FastAPI backend, dev/demo storage, and software-only operator/UI paths.
- Approved but not yet evidenced as current implemented truth: PostgreSQL runtime storage, Docker Compose deployment, Mosquitto deployment baseline, Webots integration.
- Architecture must remain portable across Raspberry Pi 4 and fallback Raspberry Pi Model B+ / 3B+ assumptions until exact hardware is confirmed.
- Interfaces must be defined before implementation claims are made.
- Legacy materials remain reference inputs, not implementation evidence.

## Fixed Safety Principles
- Safety-relevant behavior must fail to a non-motion state when control state is uncertain.
- Manual supervision is assumed for MVP.
- MVP must not claim industrial safety certification or safety integrity that is not evidenced.
- Emergency-stop, power, and hardware interlock behavior are NOT VERIFIED until confirmed on actual hardware.
- Safety assumptions and safety limitations must be written explicitly in each implementation stage report.

## Fixed Simulation-First Principle
- Simulation is the first execution target.
- Functional software-only simulation is evidenced now.
- Webots remains an approved direction, but is NOT evidenced as current implemented scope in this repository baseline.
- No hardware-dependent implementation may block progress on architecture, interfaces, or backend/server preparation.
- Simulation evidence is valid only for simulation claims, not for physical AGV claims.

## Target and Fallback Hardware Strategy
- Target onboard platform: Raspberry Pi 4.
- Fallback onboard platforms: Raspberry Pi Model B+ and Raspberry Pi 3B+.
- Exact final Raspberry Pi model is NOT CONFIRMED.
- Stage 0 decisions must preserve compatibility assumptions and avoid hard-coding a specific board revision.

## Fixed MVP Scenarios
- Operator issues supervised motion-related command through approved control path.
- Edge layer receives command through MQTT and prepares bounded actuation decision path.
- Edge layer publishes status and telemetry to server side.
- Server persists telemetry and exposes operator-visible system state.
- Software-only run produces evidence artifacts for repeatable validation.

## Stage Progression Rule
No next stage may begin as an implementation stage until the current stage gate is explicitly closed in the relevant stage report.
