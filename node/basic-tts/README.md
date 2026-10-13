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

## Transcribe a recording

The same executable supports a recording-to-text workflow using the official Node SDK. Install `@giggy-ai/sdk@0.1.1` in your application after publication, or install the SDK source checkout. STT requires Node.js 22+.

Prepare a recording that you are authorized to process:

```bash
ffmpeg -i call.mp3 -ac 1 -ar 16000 -c:a pcm_s16le recording.wav
ffprobe -v error -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 recording.wav
export GIGGY_API_KEY="YOUR_API_KEY"
node node/basic-tts/index.mjs --stt recording.wav --mode batch --output transcript.txt
```

Run the Node command from this repository's root with the SDK installed where Node can resolve it. The program logs its UUID, waits for durable completion, and writes the canonical text. Batch is free for 0.5–60 seconds; use paid `--mode fast` for longer recordings, up to 12 hours. Use paid `--mode streaming` for early provisional text: previews go to stderr, while stdout and transcript.txt receive only the final result.

The program's waits are bounded by AbortSignals. A timeout/abort stops the client wait and does not cancel an uploaded recording. Keep the logged UUID and inspect it before submitting another request. No upload or frame is retried automatically. EOF alone is not proof of success; the final generation/result checks provide that proof.

To review an exported phone call, search the saved transcript for a specific phrase and confirm it against the recording. This is text matching, not speaker attribution or sentiment analysis. Giggy does not provide a telephone transport in this example. Your application's saved transcript has its own privacy and deletion obligations.

See the [SDK method reference and migration guide](https://github.com/giggy-ai/giggy-js#transcription-method-reference).
