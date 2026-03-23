# Integration Evidence + MVP Freeze

Stage 7 consolidates the existing software-only AGV Denford contour into a repeatable end-to-end integration path.

What it does:
- runs the full local chain `operator -> backend -> MQTT -> edge -> MQTT -> backend -> operator`;
- captures repeatable software-only scenario evidence;
- freezes the MVP contour before any hardware trip or board-specific binding;
- documents what is frozen and what is intentionally deferred.

What it does not do:
- it does not add GPIO or Raspberry Pi specific runtime code;
- it does not bind to real AGV wiring;
- it does not add Webots or hardware integration;
- it does not replace Stage 2 through Stage 6 source-of-truth modules.

This zone is for repeatable integration evidence and MVP freeze only.
