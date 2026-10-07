# Stream Giggy TTS with Node.js

Giggy is a text-to-speech API for voice agents and voice-enabled products.

This example streams raw PCM speech from Giggy directly to disk without buffering the complete audio response.

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

## Run

```bash
node index.mjs
```

The example progressively writes:

```text
speech.pcm
```

Audio format:

```text
PCM16 little-endian
mono
24000 Hz
```

The request uses:

```text
mode=streaming
output_format=pcm_24000
```

## Authentication

The request sends:

```text
xi-api-key: $GIGGY_API_KEY
```

The progressive streaming endpoint rejects `Idempotency-Key`; this example intentionally does not send one.

## Source

The complete runnable example is:

```text
index.mjs
```

Documentation:

https://giggy.ai/docs/speech-api
