# Trusted Local Only Policy

## Meaning
- The current MVP is trusted local only.
- It is allowed to run as a local software contour on one developer-controlled machine.
- It is not proven for remote, unattended, field, or lab hardware operation.

## What Trusted Local Only Covers
- Local broker-backed exchange.
- Local backend, API, WebSocket, and UI.
- Local software-only integration evidence.
- Local review and demonstration use.

## What Trusted Local Only Does Not Cover
- Multi-host deployment.
- Network-hardening assumptions.
- Hardware attachment.
- Real actuator or sensor control.
- Safety-critical deployment.

## Reviewer Implication
- Local software proof is valid inside this envelope.
- Any statement outside this envelope is either deferred or forbidden until new direct evidence exists.
