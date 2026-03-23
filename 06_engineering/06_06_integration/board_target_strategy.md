# Board Target Strategy

## Fixed target statement
- Primary target board: Raspberry Pi 4.
- Secondary future portability target: Orange Pi.

## Why hardware-specific code is deferred
- Exact lab-side board and wiring details are still not fully confirmed.
- Current goal is to freeze a repeatable software-only contour first.
- Premature board binding would weaken evidence quality by mixing assumptions with unverified hardware facts.

## What must stay abstract before board binding
- GPIO access and pin numbering.
- Motor driver control interface.
- Sensor input mapping.
- Safety input wiring.
- Process supervision and deployment details tied to board OS/image specifics.

## What remains open for hardware phase
- Exact Raspberry Pi 4 variant and OS image.
- Real AGV motor/sensor electrical interface.
- Safety contour connection method.
- Whether Orange Pi portability is worth maintaining after first hardware proof.

## Current engineering stance
- Board-agnostic logic stays frozen.
- Hardware adapter implementation starts only in the future hardware phase.
- No runtime behavior should depend on Raspberry Pi vs Orange Pi at this stage.
