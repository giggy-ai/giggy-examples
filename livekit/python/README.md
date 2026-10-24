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
POST https://api.giggy.ai/v1/audio/speech
```

The LiveKit OpenAI client receives that endpoint by using:

```text
base_url=https://api.giggy.ai/v1
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

Giggy is contributing native Python TTS and WebSocket STT providers to LiveKit Agents.

Upstream PR:
https://github.com/livekit/agents/pull/7659

This directory remains the OpenAI-compatible integration example.

The native plugin is not considered officially released until the upstream
contribution is merged and an installable release is published.

## Adding STT to the surrounding agent

The TTS provider above accepts text; it does not accept microphone audio. For recorded audio, run the [Python STT walkthrough](../../python/basic-tts/README.md#transcribe-a-recording). For live audio, the [Python SDK microphone guide](https://github.com/giggy-ai/giggy-python#live-microphone-pcm-session) provides the existing Giggy PCM session contract.

The production audit found that LiveKit's default retry policy can submit four synthesis attempts after a failure without an idempotency header. Review retry configuration before using this example for paid workloads; an ambiguous timeout is not proof the first generation stopped. The [Pipecat adapter](https://github.com/giggy-ai/pipecat-giggy#speech-to-text) is the existing Giggy live STT integration. See the [developer tool guide](https://giggy.ai/docs/speech-api#api-developer-tools) for other workflows.

For live STT, install the native plugin from the linked PR source and set `stt=giggy.STT(language="en")` in your existing `AgentSession`. It uses `wss://api.giggy.ai/v1/audio/transcriptions`, resamples real mono PCM to 16 kHz, applies Silero endpointing, overlaps decode preparation with endpoint confirmation, and verifies final input, transcript identity and saved results. Keep consuming the stream and surface verification errors after a final event. Each source-adapter utterance is 0.5–30 seconds; cancellation aborts unfinished work without replay. Keep application turn detection, interruption handling and room transport in your existing agent.

The example in this directory remains OpenAI-compatible TTS. The native Giggy source plugin is not yet an upstream release; do not assume a package-registry install contains it. Changing an OpenAI transcription base URL does not migrate STT. See the [partner integration guide](../../README.md#partner-integrations) for current source and protocol status.
