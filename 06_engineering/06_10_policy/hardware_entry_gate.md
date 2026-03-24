# Hardware Entry Gate

## Gate Status
- Current status: BLOCKED
- Reason: the project is still only evidenced as a software-only MVP.

## Minimum Prerequisites Before First Honest Hardware Phase
- Confirmed board facts:
  - exact available board model,
  - storage medium facts,
  - OS/runtime constraints,
  - available communication interfaces.
- Confirmed power path facts:
  - supply voltage/current expectations,
  - power source path,
  - safe power-on and power-off constraints.
- Confirmed ESTOP chain understanding:
  - what is hardwired,
  - what remains local safety contour,
  - what software must not bypass.
- Confirmed motor and sensor interface facts:
  - drive interface type,
  - sensor types,
  - connector identities,
  - signal level constraints,
  - what remains unknown.
- Confirmed allowed lab procedure:
  - what the lab allows to inspect,
  - what may be connected,
  - what may not be energized or moved,
  - who must supervise.
- Confirmed evidence capture plan:
  - what photos must be taken,
  - what notes must be recorded,
  - what logs must be saved,
  - what initial tests are allowed.

## Gate Must Remain Closed If Any Of These Are Missing
- board facts not confirmed,
- power path not understood,
- ESTOP chain not understood,
- motor/sensor interfaces not surveyed,
- lab procedure not approved,
- first-lab evidence plan not prepared.

## What This Gate Does Not Mean
- It does not mean hardware control is immediately authorized.
- It does not mean motion tests are immediately authorized.
- It does not mean safety is proven.
- It only means the project may begin an honest hardware survey phase.
