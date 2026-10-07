# Giggy TTS examples

[![Examples CI](https://github.com/GRQDigitalCapital/giggy-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/GRQDigitalCapital/giggy-examples/actions/workflows/ci.yml)

Giggy is a text-to-speech (TTS) API for developers building voice agents and voice-enabled products.

This repository contains small, runnable Giggy TTS examples for:

- Node.js
- Python
- Streaming text-to-speech
- OpenAI-compatible clients
- LiveKit
- Pipecat
- Vapi
- Model Context Protocol (MCP)

## Developer resources

- Documentation: https://giggy.ai/docs/speech-api
- OpenAPI 3.1: https://giggy.ai/v1/openapi.json
- JavaScript/TypeScript SDK: https://github.com/giggy-ai/giggy-js
- MCP endpoint: https://giggy.ai/mcp
- Pricing: https://giggy.ai/pricing
- MCP setup repository: https://github.com/GRQDigitalCapital/giggy-mcp

## Quick start

Set a Giggy API key and voice UUID:

```bash
export GIGGY_API_KEY="giggy_sk_..."
export GIGGY_VOICE_ID="your-giggy-voice-uuid"
```

Generate an MP3 with the native Giggy text-to-speech REST API:

```bash
curl --fail --show-error \
  --request POST "https://giggy.ai/v1/text-to-speech" \
  --header "xi-api-key: ${GIGGY_API_KEY}" \
  --header "content-type: application/json" \
  --header "idempotency-key: quickstart-$(date +%s)-$$" \
  --data "{\"text\":\"Hello from Giggy.\",\"voice_id\":\"${GIGGY_VOICE_ID}\",\"model_id\":\"giggyspeech\",\"mode\":\"batch\",\"output_format\":\"mp3_24000_160\",\"voice_settings\":{\"speed\":1}}" \
  --output speech.mp3
```

For framework-specific integrations, use the examples below.

## Core API endpoints

Native Giggy text-to-speech:

```text
POST https://giggy.ai/v1/text-to-speech
```

OpenAI-compatible text-to-speech:

```text
POST https://giggy.ai/v1/audio/speech
```

Public voice discovery:

```text
GET https://giggy.ai/v1/voices
```

Public connector voice catalog:

```text
GET https://giggy.ai/v1/integrations/voices
```

Vapi custom TTS:

```text
POST https://giggy.ai/v1/integrations/vapi/text-to-speech/{voiceId}
```

MCP:

```text
https://giggy.ai/mcp
```

## Authentication

The native Giggy REST API uses:

```text
xi-api-key: $GIGGY_API_KEY
```

The OpenAI-compatible API, Vapi adapter, and MCP use:

```text
Authorization: Bearer $GIGGY_API_KEY
```

Keep Giggy API keys server-side.

## Environment

Set:

```bash
export GIGGY_API_KEY="giggy_sk_..."
export GIGGY_VOICE_ID="your-giggy-voice-uuid"
```

You can get a public voice UUID from:

```text
GET https://giggy.ai/v1/voices
```

## Examples

| Example | Directory |
| --- | --- |
| Native Node.js Batch TTS | [node/basic-tts/](node/basic-tts/) |
| Native Node.js Streaming TTS | [node/streaming-tts/](node/streaming-tts/) |
| OpenAI-compatible Node.js | [node/openai-compatible/](node/openai-compatible/) |
| Native Python Batch TTS | [python/basic-tts/](python/basic-tts/) |
| LiveKit Python | [livekit/python/](livekit/python/) |
| Pipecat Python | [pipecat/python/](pipecat/python/) |
| Vapi custom TTS | [vapi/](vapi/) |
| MCP | [mcp/](mcp/) |

## Node.js: Batch TTS

Run:

```bash
node node/basic-tts/index.mjs
```

The example writes:

```text
node/basic-tts/speech.mp3
```

Batch TTS uses Giggy's zero-credit Batch mode.

## Node.js: Streaming TTS

Run:

```bash
node node/streaming-tts/index.mjs
```

The example progressively writes raw:

```text
PCM16 little-endian
mono
24000 Hz
```

to:

```text
node/streaming-tts/speech.pcm
```

Streaming mode uses the applicable paid Giggy speech mode.

## OpenAI-compatible Node.js

Install:

```bash
cd node/openai-compatible
npm install
```

Run:

```bash
node index.mjs
```

The example uses the official OpenAI JavaScript client but points it at:

```text
https://giggy.ai/v1
```

No OpenAI API key is required. Use your Giggy API key.

## Python: Batch TTS

Run:

```bash
python python/basic-tts/main.py
```

This example uses only the Python standard library.

## LiveKit

See:

```text
livekit/python/README.md
```

Giggy works with LiveKit's OpenAI-compatible TTS plugin by setting a custom API base URL.

This is a compatibility integration, not a native Giggy provider listing in LiveKit.

## Pipecat

See:

```text
pipecat/python/README.md
```

The Pipecat example uses a small `TTSService` adapter because Pipecat's current built-in OpenAI TTS implementation validates voices against OpenAI's own named voice set before making a request.

Giggy voices use UUIDs.

This is a compatibility integration, not a native Giggy provider listing in Pipecat.

## Vapi

See:

```text
vapi/README.md
```

Giggy implements Vapi's custom TTS webhook contract.

This is a custom TTS integration, not a native Giggy provider listing in Vapi.

## MCP

See:

```text
mcp/README.md
```

and the dedicated repository:

```text
https://github.com/GRQDigitalCapital/giggy-mcp
```

## Pricing modes

Giggy currently exposes:

```text
batch
fast
streaming
```

Batch generation uses zero credits.

Fast, Streaming, OpenAI-compatible, Vapi, and other realtime compatibility paths use the applicable paid speech mode described in Giggy's current documentation.

Always use the live pricing page as the pricing source of truth:

```text
https://giggy.ai/pricing
```
