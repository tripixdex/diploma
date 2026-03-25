# Lab No-Go Actions

## Purpose
- Keep the first lab visit a survey mission.
- Prevent unsafe improvisation.
- Prevent bluffing after partial observation.

## Forbidden First-Lab Actions
- No direct motor-command experiments.
- No direct GPIO toggling on unknown lines.
- No direct signal injection into unknown connectors.
- No casual powering of unknown paths.
- No rewiring of unknown connectors.
- No bypassing or probing around incomplete ESTOP understanding.
- No deploying board-specific runtime code.
- No claiming pin mapping without direct evidence.
- No claiming board-binding readiness from photos alone.
- No "let's just try" behavior when board, power, or safety facts are incomplete.

## Immediate Stop Conditions
- Power path cannot be explained safely.
- ESTOP chain observations are unclear.
- Ownership or supervision of the hardware is unclear.
- Lab staff prohibit a requested action.
- A connector or interface cannot be identified but someone proposes energizing or driving it anyway.

## Post-Visit Wording Boundary
- If only photos were collected, say only photos were collected.
- If a fact was verbal only, mark it verbal only.
- If a field stayed unknown, say unknown.
- No survey result may be described as integration readiness.
