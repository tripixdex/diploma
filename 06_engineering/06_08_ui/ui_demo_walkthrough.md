# UI Demo Walkthrough

## Main Screen In Plain Language
- The top card answers: what state is the system in, is the link alive, and what should the operator do next.
- The control card answers: what button to press first, what values to enter, and how to tell whether the command was only sent or truly accepted.
- The lower cards answer: what just happened, what commands were seen, what motion evidence exists, and what live updates are coming now.

## Recommended Manual Demo Order
1. Open the UI and point at the main state card.
2. Read the short explanation aloud: the screen should tell a non-developer what is happening now.
3. Show the operator flow card on the right: first choose mode, then send movement, then observe result.
4. Send `MANUAL` mode.
5. Show that the command first appears as dispatched, then later as accepted or rejected based on event evidence.
6. Send a small manual command such as `0.15 m/s` and `0.00 rad/s`.
7. Point at telemetry snapshot and live activity to show that the backend and MQTT path reacted.
8. Try the reset action and show the honest rejection if the contract blocks it.
9. Let heartbeat loss push the system into degraded mode and show that the top card explains the situation in plain language.

## What The Supervisor Sees
- one calm screen instead of raw console logs;
- obvious current state and next step;
- compact human-readable events with optional raw debug details;
- honest visibility of accepted, rejected, and degraded outcomes.

## What This Proves
- backend REST + WebSocket are usable by a human-facing client;
- operator commands still go through the frozen MVP chain;
- the UI no longer hides cause and effect behind developer language.

## What This Does Not Prove
- real Raspberry Pi binding;
- real AGV wiring;
- GPIO access;
- hardware-phase performance.
