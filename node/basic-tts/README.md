# Use Giggy TTS with Node.js

Giggy is a text-to-speech API for voice agents and voice-enabled products.

This example uses Giggy's native REST text-to-speech API from Node.js with the built-in `fetch` API.

## Endpoint

```text
POST https://giggy.ai/v1/text-to-speech
```

## Requirements

- Node.js 22+
- Giggy API key
- Giggy voice UUID

## Environment

```bash
export GIGGY_API_KEY="giggy_sk_..."
export GIGGY_VOICE_ID="your-giggy-voice-uuid"
```

A public voice UUID can be obtained from:

```text
GET https://giggy.ai/v1/voices
```

## Run

```bash
node index.mjs
```

The example writes:

```text
speech.mp3
```

It uses Giggy's Batch speech mode.

## Authentication

The request sends:

```text
xi-api-key: $GIGGY_API_KEY
```

and a unique:

```text
idempotency-key
```

## Source

The complete runnable example is:

```text
index.mjs
```

Documentation:

https://giggy.ai/docs/speech-api

OpenAPI:

https://giggy.ai/v1/openapi.json
