# Pre-Hardware Checklist

## Before the first lab trip
- Confirm permission, time window, and physical access to the Denford platform.
- Confirm whether Raspberry Pi 4 can be used as the first binding target.
- Confirm whether any Orange Pi check is needed at all in the first lab visit.
- Print or bring the current contract, board strategy, and frozen MVP manifest.

## Photos to take
- Full robot overview from multiple sides.
- Existing control cabinet or electronics compartment.
- Power input path and power conversion modules.
- Motor driver labels and connector areas.
- Sensor boards, line sensors, docking sensors, obstacle sensor placements.
- Emergency stop chain, relays, safety contacts, and wiring labels.
- Any available onboard computer mounts or integration points.

## Interfaces to confirm
- Motor driver control interface type.
- Sensor output signal types and voltage levels.
- Emergency stop wiring semantics.
- Available serial, USB, UART, SPI, I2C, or GPIO exposure points.
- Grounding and power reference constraints.

## Raspberry Pi 4 facts to capture
- Available supply voltage/current budget for onboard computer.
- Mounting space and cable routing feasibility.
- Cooling constraints and enclosure conditions.
- Whether Ethernet, Wi-Fi, or both are realistically available.
- Any EMI or isolation constraints near the control electronics.

## Orange Pi questions to close
- Is Orange Pi needed at all, or only as a future portability note?
- Are there any lab reasons to prefer it over Raspberry Pi 4?
- Would Orange Pi introduce avoidable driver or deployment risk at this phase?

## Signals, connectors, power, and ESTOP
- Confirm traction enable signal path.
- Confirm motion command interface expectations.
- Confirm how local safe stop and emergency stop are latched.
- Confirm whether emergency stop must remain entirely outside software control.
- Confirm connector types, spare channels, and voltage domains.

## Evidence artifacts to collect in the lab phase
- Labeled photos.
- Handwritten or digital I/O mapping notes.
- Board photos with connector annotations.
- Power measurements or manufacturer label captures.
- Safety contour notes approved by the lab/supervisor.
- A first hardware survey report linked back to the contract docs.
