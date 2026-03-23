# Stage 7B Polish Zone

This directory contains the polished software-only demo package prepared after the frozen MVP contour from Stage 7.

It is used to:
- explain the demo in a supervisor-friendly order;
- run one honest end-to-end software-only demonstration;
- freeze what may and may not change before the hardware phase;
- prepare the first lab trip checklist without writing hardware-specific code.

It does not contain:
- GPIO or Raspberry Pi runtime code;
- Orange Pi specific code;
- Webots integration;
- backend, transport, edge, or twin rewrites.

Source logic remains in:
- `06_engineering/06_01_sim_twin/`
- `06_engineering/06_02_edge/`
- `06_engineering/06_03_transport/`
- `06_engineering/06_04_backend/`
- `06_engineering/06_05_operator/`
- `06_engineering/06_06_integration/`
