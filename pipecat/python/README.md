# Use Giggy TTS with Pipecat

Giggy exposes an OpenAI-compatible text-to-speech endpoint:

```text
POST https://giggy.ai/v1/audio/speech
```

Giggy voices use UUID identifiers.

Pipecat's current built-in OpenAI TTS service validates the voice against OpenAI's own named voice set before making the HTTP request.

For that reason, this example uses a small native Pipecat `TTSService` adapter instead of `OpenAITTSService`.

This is a compatibility integration.

Giggy is not claiming a native Pipecat provider listing.

## Requirements

- Python 3.11+
- Giggy API key
- Giggy voice UUID

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Example

```python
import aiohttp

from giggy_tts import GiggyTTSService


async def create_tts():
    session = aiohttp.ClientSession()

    tts = GiggyTTSService(
        api_key=r"""giggy_sk_...""",
        voice_id=r"""00000000-0000-0000-0000-000000000000""",
        aiohttp_session=session,
        sample_rate=24000,
    )

    return session, tts
```

Use the returned `tts` service in the same place in your Pipecat pipeline where you would use another TTS service.

The application that creates the `aiohttp.ClientSession` owns that session and must close it during application shutdown.

## Audio

The adapter requests:

```text
PCM16
mono
24000 Hz by default
```

Supported Giggy compatibility sample rates are:

```text
8000
16000
22050
24000
```

## Authentication

The adapter sends:

```text
Authorization: Bearer $GIGGY_API_KEY
```

## Validate installation

```bash
python smoke_test.py
```

The smoke test constructs the Pipecat service without performing synthesis.
