# Use Giggy TTS with LiveKit

Giggy exposes an OpenAI-compatible speech endpoint.

LiveKit's OpenAI TTS plugin supports a custom API base URL, API key, model, voice string, and response format, so Giggy can be used as the TTS component of a LiveKit voice agent without modifying LiveKit.

This is a compatibility integration.

Giggy is not claiming a native LiveKit provider listing.

## Requirements

- Python 3.10+
- Giggy API key
- Giggy voice UUID

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment

```bash
export GIGGY_API_KEY="giggy_sk_..."
export GIGGY_VOICE_ID="your-giggy-voice-uuid"
```

## Create the TTS provider

```python
from giggy_tts import create_giggy_tts


tts = create_giggy_tts()
```

## Use it in an existing AgentSession

```python
from livekit.agents import AgentSession

from giggy_tts import create_giggy_tts


session = AgentSession(
    tts=create_giggy_tts(),
)
```

Configure your LLM, STT, room transport, VAD, and turn detection separately.

This repository deliberately demonstrates only the Giggy TTS integration.

## Giggy endpoint used

```text
POST https://giggy.ai/v1/audio/speech
```

The LiveKit OpenAI client receives that endpoint by using:

```text
base_url=https://giggy.ai/v1
model=giggyspeech
voice=<Giggy voice UUID>
response_format=pcm
```

## Validate installation

```bash
python smoke_test.py
```

The smoke test constructs the TTS object but performs no synthesis.

## Native LiveKit plugin contribution

Giggy is contributing a native Python TTS plugin to LiveKit Agents.

Upstream PR:
https://github.com/livekit/agents/pull/7659

This directory remains the OpenAI-compatible integration example.

The native plugin is not considered officially released until the upstream
contribution is merged and an installable release is published.

## Adding STT to the surrounding agent

The TTS provider above accepts text; it does not accept microphone audio. For recorded audio, run the [Python STT walkthrough](../../python/basic-tts/README.md#transcribe-a-recording). For live audio, the [Python SDK microphone guide](https://github.com/giggy-ai/giggy-python#live-microphone-pcm-session) provides the existing Giggy PCM session contract.

The production audit found that LiveKit's default retry policy can submit four synthesis attempts after a failure without an idempotency header. Review retry configuration before using this example for paid workloads; an ambiguous timeout is not proof the first generation stopped. The [Pipecat adapter](https://github.com/giggy-ai/pipecat-giggy#speech-to-text) is the existing Giggy live STT integration. See the [developer tool guide](https://giggy.ai/docs/speech-api#api-developer-tools) for other workflows.

Keep the Giggy key on the LiveKit agent server. Resample incoming audio to PCM16 mono 16 kHz, wait for microphone_ready, send ordered acknowledged frames and read SSE concurrently. Map cumulative transcript_chunk revisions to your application's provisional transcription state, then reconcile durable completion before using final text. LiveKit's VAD, turn detection, interruption handling and room transport remain responsibilities of your agent implementation. One Giggy live session accepts at most 30 seconds and must finish within 35 seconds of readiness.

This repository does not ship a native Giggy LiveKit STT provider. Do not set an arbitrary OpenAI transcription base URL and assume its request/event schema matches Giggy. The existing native TTS contribution and this STT protocol guide have separate verification/acceptance status.
