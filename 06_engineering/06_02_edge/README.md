# Edge MVP

## What This Stage Is
This directory contains the Stage 3 edge-oriented runtime MVP for AGV Denford. It is a local onboard logic layer that sits between external command/event sources and the contract-driven state machine.

## What It Does
- accepts edge-level commands and local events;
- applies contract-aligned state transitions through the existing twin domain logic;
- enforces a hardware-agnostic adapter boundary;
- models heartbeat supervision and degraded link behavior;
- rejects unsafe commands locally before any hardware-specific execution path exists;
- runs entirely in local in-memory mode.

## What It Does Not Do
- no real MQTT transport;
- no real GPIO or Raspberry Pi hardware access;
- no real HardwareAdapter implementation against Denford wiring;
- no backend, UI, Docker, or Webots scene;
- no hardware-dependent claim beyond contract-level edge behavior.

## Relation to Earlier Stages
- Stage 1 fixed the system contract that defines states, events, MQTT semantics, and safety principles.
- Stage 2 proved the state machine contract through a functional twin.
- Stage 3 introduces an edge-oriented runtime layer that reuses the established domain logic but still remains transport-free and hardware-agnostic.
