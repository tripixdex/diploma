# Pre-Hardware Operating Policy

## Current Operating Envelope
- The current project contour is a software-only MVP.
- The current contour is trusted local only.
- The current contour is intended for local demonstration, review, and software evidence collection.
- The current contour is not a hardware-ready runtime.
- The current contour is not a deployment-ready system.
- The current contour is not a real-AGV safety proof.

## What Operation Is Allowed Now
- Local software-only runs on a developer machine.
- Local reviewer demos using the frozen software MVP.
- Local integration and evidence runs already covered by the software-only baseline.
- Documentation, packaging, evidence, and policy hardening that does not expand scope.

## What Operation Is Not Allowed To Be Claimed Now
- That this software stack is ready to control the real AGV.
- That this software stack is ready for unattended deployment.
- That this software stack is ready for production or industrial use.
- That current local safety behavior proves real AGV safety.
- That board binding already exists beyond hardware-agnostic abstraction.

## Trusted Local Only Meaning
- Local machine setup is part of the current operating assumption.
- Local broker, local backend, local UI, and local runners are acceptable for evidence.
- Remote deployment, multi-host deployment, and hardware deployment are outside the current proven envelope.

## Hardware Policy Boundary
- No honest hardware phase begins until the hardware entry gate is explicitly satisfied.
- The future hardware phase must start with factual survey and evidence capture, not with immediate control experiments.
- The first lab visit must follow the hardware survey packet and remains survey-only.
- Survey activity does not authorize GPIO, motion, or board-binding experimentation.

## Reviewer Note
- This policy is intended to make bluffing impossible at the repo level.
- If a statement exceeds this operating envelope, it must be treated as deferred or forbidden.
