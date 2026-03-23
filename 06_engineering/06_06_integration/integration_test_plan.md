# Integration Test Plan

## Stage 7 verifies
- full local chain `operator -> backend -> MQTT -> edge -> MQTT -> backend -> operator`;
- repeatable startup and initial status retrieval;
- mode/manual command path;
- backend storage and serving path;
- operator live update path;
- degraded transition on heartbeat timeout;
- invalid command rejection path;
- current reset/clear behavior according to the frozen contract.

## Stage 7 does not verify
- hardware integration;
- GPIO or Raspberry Pi specific runtime behavior;
- Webots integration;
- final lab deployment;
- production reliability under long-running field conditions.

## Mandatory evidence before closeout
- integration runner completes without false success claims;
- degraded path is observable end-to-end;
- invalid command rejection is observable end-to-end;
- reset/clear path behavior is recorded honestly;
- Stage 2 through Stage 6 regressions remain green.
