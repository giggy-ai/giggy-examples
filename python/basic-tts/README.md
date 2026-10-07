# Use Giggy TTS with Python

Giggy is a text-to-speech API for voice agents and voice-enabled products.

This example generates an MP3 using Giggy's native REST API and only the Python standard library.

No third-party Python HTTP dependency is required.

## Endpoint

```text
POST https://giggy.ai/v1/text-to-speech
```

## Requirements

- Python 3.10+
- Giggy API key
- Giggy voice UUID

## Environment

```bash
export GIGGY_API_KEY="giggy_sk_..."
export GIGGY_VOICE_ID="your-giggy-voice-uuid"
```

## Run

From the repository root:

```bash
python python/basic-tts/main.py
```

Or from this directory:

```bash
python main.py
```

The example writes:

```text
speech.mp3
```

The request uses:

```text
model_id=giggyspeech
mode=batch
output_format=mp3_24000_160
```

Authentication:

```text
xi-api-key: $GIGGY_API_KEY
```

The request also sends a unique idempotency key.

The complete runnable implementation is:

```text
main.py
```

Documentation:

https://giggy.ai/docs/speech-api
