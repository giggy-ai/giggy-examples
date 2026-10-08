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

This integration is maintained by Giggy, the speech API provider. The repository
uses the permissive ISC license. Last tested with Pipecat 1.12.0 and Python 3.12.

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

```python
from pipecat.pipeline.pipeline import Pipeline

# Use the service returned by create_tts() with your existing processors.
pipeline = Pipeline([transport.input(), stt, llm, tts, transport.output()])
```

The surrounding transport, STT and LLM belong to your existing application.
Pipecat initializes the audio rate when it sets up the pipeline; use the service
through the pipeline rather than calling `run_tts` on an uninitialized service.

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

Each synthesis submits complete text and receives progressive audio over HTTP.
Incremental text input over WebSocket is not supported. Requests use paid
Streaming admission; automatic retries and redirects are disabled, and no
`Idempotency-Key` is sent. The adapter does not select an alternate provider.

PCM16 samples are aligned across transport chunks. Empty audio, truncated
samples, unexpected content types, HTTP failures and timeouts yield an
`ErrorFrame`. Errors omit response bodies and transport details that could expose
credentials. Cancellation propagates and closes the active HTTP response.

## Validate installation

```bash
python smoke_test.py
```

The smoke test constructs the Pipecat service without performing synthesis.

The existing `live_smoke.py` exercises the Pipecat pipeline and makes one paid
synthesis request. Run it only when you explicitly authorize that charge:

```bash
export GIGGY_API_KEY="your-api-key"
export GIGGY_VOICE_ID="your-voice-uuid"
export GIGGY_ALLOW_BILLABLE_SMOKE=1
python live_smoke.py
```

## Integration changelog

- 2026-10-07: align PCM samples, reject malformed/empty audio and invalid speed,
  add bounded read/connect timeouts, disable redirects, keep errors credential-safe,
  and exercise the configured pipeline in the gated live smoke test.
