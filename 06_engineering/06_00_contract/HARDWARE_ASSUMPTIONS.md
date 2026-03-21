# Hardware Assumptions

## Current Assumption Status
- Exact Raspberry Pi model for the final AGV Denford MVP is unknown.
- Target hardware assumption: Raspberry Pi 4.
- Fallback hardware assumptions: Raspberry Pi Model B+ and Raspberry Pi 3B+.
- Final hardware selection is NOT CONFIRMED at Stage 0.

## Consequences for Architecture
- The architecture must not depend on one exact Raspberry Pi revision.
- Hardware access must be isolated from transport, application logic, and server integration.
- Performance-sensitive assumptions must remain conservative until measured.
- GPIO, serial, timing, startup, and deployment behavior must be abstracted away from business logic.
- Docker usage on edge must remain optional until the final Pi model and resource budget are confirmed.

## HardwareAdapter Boundary
The following concerns must be abstracted behind a future `HardwareAdapter` boundary:

- GPIO read/write and pin mapping.
- Motor control output interface.
- Sensor input acquisition.
- Safe startup and safe shutdown transitions.
- Emergency-stop and interlock input integration.
- Board-specific timing or debounce behavior.
- Board-specific library binding choice.
- Board-specific device discovery and health checks.

## Open Questions for Supervisor or Lab
- Which exact Raspberry Pi model will be available for final validation?
- What motor driver and electrical interface are actually available on the AGV side?
- Which sensors are physically connected and still operational?
- Is there a stable power budget and startup sequence for the onboard computer?
- Is there a required OS image, Python version, or lab policy for deployment?
- Are there mandatory safety restrictions for motion testing in the lab?

## What Can Be Done Before Hardware Confirmation
- Freeze architecture and repo execution rules.
- Define stage gates and reporting discipline.
- Prepare simulation-first workflow in Webots.
- Define software boundaries for edge, transport, server, and telemetry.
- Prepare deployment assumptions that remain hardware-agnostic where possible.
- Separate implementation evidence from legacy and reference materials.

## What Must Not Be Claimed Before Confirmation
- Exact GPIO map for the final robot.
- Exact deployment profile on the final Pi model.
- Real-time performance guarantees on hardware.
- Verified emergency-stop integration.
- Verified hardware motion behavior.
