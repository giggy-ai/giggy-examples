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
