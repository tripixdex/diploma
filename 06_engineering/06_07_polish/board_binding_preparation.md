# Board Binding Preparation

## Primary target
- Raspberry Pi 4 is the primary board target for the first hardware-binding phase.

## Secondary portability target
- Orange Pi is not the current binding target.
- Orange Pi remains only a secondary portability target for a later phase if needed.

## Why Raspberry Pi 4 is primary
- It matches the approved project direction.
- It has lower integration risk for the first real hardware phase.
- It is sufficient for the current MVP contour without forcing early board divergence.
- It keeps the hardware-binding phase focused on one target instead of splitting effort.

## Why Orange Pi is deferred
- It would add avoidable variability before the first hardware evidence is collected.
- Board-specific differences are not relevant until real interfaces and deployment constraints are confirmed.
- There is no current evidence-based reason to switch the primary target away from Raspberry Pi 4.

## What must stay abstract before board-specific code
- GPIO pin mapping.
- Sensor voltage and signal handling.
- Motor driver control binding.
- ESTOP observation path.
- Board-specific service management.
- Board-specific network startup assumptions.
- Board-specific deployment packaging.

## Facts still to confirm before binding
- Exact Raspberry Pi 4 variant and available peripherals.
- Power budget and connector availability on the real AGV.
- Required isolation or signal conditioning.
- Real sensor signal semantics and voltage levels.
- Real motor driver input expectations.
- Physical installation constraints and cooling.
