# Open Questions

## Open Hardware Questions
- Which exact Raspberry Pi model will be available for final deployment and validation?
- What motor driver or actuator control interface is present on the real AGV?
- Which sensors are still installed, electrically accessible, and operational on the Denford platform?
- How is the local emergency-stop circuit wired relative to the onboard controller?
- Is there a dedicated traction enable/disable line or only indirect motor command inhibition?

## Open Lab Questions
- What physical access to the AGV and lab space will be available during later stages?
- Are there restrictions on powered motion testing in the lab?
- Is there a mandated OS image, Python version, or deployment policy for Raspberry Pi hardware?
- Can broker/backend services run on lab-local infrastructure, or only on a developer workstation?

## Open Signal Mapping Questions
- Exact GPIO or alternative bus mapping for line sensors, docking sensors, obstacle sensor, and e-stop.
- Signal polarity, debounce requirements, sampling rate, and sensor health semantics.
- Whether docking and obstacle signals come directly from sensors or through an intermediate controller.
- What heartbeat/link status can be measured directly on edge versus inferred from MQTT session state.

## Raspberry Pi Status
- Exact Raspberry Pi model remains pending.
- Contract work assumes Raspberry Pi 4 as target and Raspberry Pi Model B+ / 3B+ as fallback only at the architecture level.

## What Can Proceed Without These Answers
- State machine freezing.
- MQTT topic and payload contract freezing.
- Logical I/O grouping and `HardwareAdapter` boundary definition.
- Webots simulation scaffold preparation in Stage 2.
- Backend/operator contract planning at interface level only.

## What Is Blocked By These Answers
- Final GPIO map and board-specific adapter implementation.
- Electrical integration claims for real AGV hardware.
- Timing and performance claims on physical hardware.
- Verified e-stop, obstacle, and docking integration on the real robot.
- Final deployment profile for the exact Raspberry Pi revision.
