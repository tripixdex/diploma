# Transport Architecture

## Purpose
The Stage 4 transport layer provides the first real broker-backed exchange for the project. It does not replace edge logic; it carries contract-shaped messages between a local operator-side publisher, a transport-facing edge gateway, and transport observers.

## Main Components
- `mqtt_client_config.py`: broker settings, topic policy, QoS, and retained behavior.
- `mqtt_message_codec.py`: JSON payload shaping and decoding according to `MQTT_CONTRACT.md`.
- `mqtt_transport_runner.py`: local demo broker, edge gateway, operator publisher, and observer clients.

## Boundaries
- Codec boundary: message structure, field defaults, JSON encode/decode.
- Config boundary: broker host/port, topic policy, client IDs, keepalive.
- Runtime boundary: transport runner owns client lifecycle, subscriptions, reconnect flow, and the bridge into Stage 3 edge runtime.

## Runtime Flow
1. Start an in-process local MQTT broker for demo validation.
2. Start the edge gateway client and subscribe it to `cmd/*` topics.
3. Bootstrap edge startup locally so the edge side publishes initial retained status.
4. Start observer clients that subscribe to status/event/heartbeat topics.
5. Publish operator commands through MQTT.
6. Decode MQTT commands into Stage 3 edge commands.
7. Let the existing edge runtime publish results back through MQTT using a transport adapter.
8. Demonstrate retained status and reconnect-tolerant behavior with a late observer and a reconnected operator publisher.

## Why This Is Still Hardware-Agnostic
The transport layer speaks only the Stage 1 MQTT contract and the Stage 3 edge API. It does not assume any Raspberry Pi GPIO layout or real Denford wiring and therefore remains portable across the still-unconfirmed target board revision.
