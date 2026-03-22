# MQTT Transport

## What This Stage Is
This directory contains the Stage 4 minimal real MQTT transport layer for AGV Denford. It is the first stage that uses a real broker-backed exchange instead of only in-memory publication.

## What It Does
- uses real `paho-mqtt` clients;
- starts a local demo broker in-process for repeatable local validation;
- bridges MQTT command topics to the existing edge runtime;
- publishes contract-shaped status, telemetry, alarm, fault, audit, and heartbeat messages;
- demonstrates broker connection, publish/subscribe exchange, retained status behavior, and reconnect-tolerant local demo flow.

## What It Does Not Do
- no backend or database;
- no operator UI;
- no GPIO or Raspberry Pi hardware binding;
- no Docker full-stack orchestration;
- no Webots scene.

## Relation to Earlier Stages
- Stage 1 fixed the MQTT contract.
- Stage 2 proved contract behavior through a local twin.
- Stage 3 introduced a local edge runtime.
- Stage 4 places a real MQTT transport layer between local components while keeping the runtime hardware-agnostic.
