# Use Giggy TTS with the OpenAI JavaScript SDK

Giggy exposes an OpenAI-compatible text-to-speech endpoint.

This example uses the official OpenAI JavaScript client while sending speech requests to Giggy.

## Giggy base URL

```text
https://giggy.ai/v1
```

The OpenAI-compatible speech route is:

```text
POST https://giggy.ai/v1/audio/speech
```

## Requirements

- Node.js 22+
- Giggy API key
- Giggy voice UUID

## Install

```bash
npm install
```

## Environment

```bash
export GIGGY_API_KEY="giggy_sk_..."
export GIGGY_VOICE_ID="your-giggy-voice-uuid"
```

## Run

```bash
node index.mjs
```

The important client configuration is:

```js
const client = new OpenAI({
  apiKey: process.env.GIGGY_API_KEY,
  baseURL: 'https://giggy.ai/v1',
  maxRetries: 0,
});
```

Speech is generated with:

```js
const response = await client.audio.speech.create({
  model: 'giggyspeech',
  voice: process.env.GIGGY_VOICE_ID,
  input: 'Hello from the Giggy OpenAI-compatible speech endpoint.',
  response_format: 'mp3',
});
```

No OpenAI API key is required.

Use the Giggy API key.

The complete runnable example is:

```text
index.mjs
```

Documentation:

https://giggy.ai/docs/speech-api
