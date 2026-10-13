# Giggy speech API examples
[![Examples CI](https://github.com/giggy-ai/giggy-examples/actions/workflows/ci.yml/badge.svg)](https://github.com/giggy-ai/giggy-examples/actions/workflows/ci.yml)

Small, runnable examples for integrating Giggy text-to-speech with Node.js, Python, LiveKit, Pipecat, Vapi, MCP, and OpenAI-compatible clients. Recorded-audio speech-to-text onboarding is documented below through the existing official SDK checkouts.

This repository contains small, runnable Giggy TTS examples for:

- Node.js
- Python
- Streaming text-to-speech
- OpenAI-compatible clients
- LiveKit
- Pipecat
- Vapi
- Model Context Protocol (MCP)

For speech-to-text, see the [Giggy Speech API guide](https://giggy.ai/docs/speech-api#api-stt-developer-path), the [Python SDK](https://github.com/giggy-ai/giggy-python), and the [Node.js/TypeScript SDK](https://github.com/giggy-ai/giggy-js). Use SDK builds that contain the transcription methods; publishing those builds is separate from this README update.

## First recorded transcript

Prepare signed PCM16 mono 16 kHz WAV, 0.5–60 seconds for free Batch. Install the updated Python SDK from its source checkout, set `GIGGY_API_KEY`, and run this from your application directory:

```python
import os
from giggy import Giggy

giggy = Giggy(api_key=os.environ["GIGGY_API_KEY"])
print(giggy.transcriptions.transcribe("recording.wav", mode="batch")["text"])
```

The SDK submits once, checks durable status, and fetches the signed transcript. For a longer paid recording, use `mode="fast"`. For provisional text from an uploaded recording, the SDKs offer `transcriptions.stream()`: every `transcript_chunk` replaces the previous preview. Live microphone capture uses the [separate PCM session contract](https://giggy.ai/docs/speech-api#api-stt-streaming). The current framework examples below cover TTS; the [Pipecat Giggy adapter](https://github.com/giggy-ai/pipecat-giggy#speech-to-text) is the existing STT integration.

## Prepare audio for STT

The current STT API accepts signed PCM16 mono 16 kHz WAV. Convert a local recording before calling either SDK:

```bash
ffmpeg -i input.mp3 -ac 1 -ar 16000 -c:a pcm_s16le recording.wav
ffprobe -v error -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 recording.wav
```

Verify `pcm_s16le`, `16000`, and `1`. Renaming an MP3 to `.wav` does not convert it. Choose Batch only for 0.5–60 seconds; use paid Fast for longer recordings. The SDKs accept local WAV paths on this API; they do not accept a remote URL or silently transcode another format.

## STT recipes using the current transcript contract

These examples use only the existing transcript text. They do not imply speaker identification, word timestamps, summaries, or sentiment analysis.

**Archive a long recording as searchable text:** after converting to `recording.wav`, run this Python code with an API key. Fast is paid.

```python
import os
from pathlib import Path
from giggy import Giggy

text = Giggy(api_key=os.environ["GIGGY_API_KEY"]).transcriptions.transcribe("recording.wav", mode="fast")["text"]
Path("recording.txt").write_text(text, encoding="utf-8")
```

**Flag a phrase in a call recording:** convert the recording to mono WAV, then inspect the final transcript for an exact phrase. This is application-side text matching; it does not classify sentiment or identify speakers.

```python
import os
from giggy import Giggy

text = Giggy(api_key=os.environ["GIGGY_API_KEY"]).transcriptions.transcribe("recording.wav", mode="fast")["text"]
print("Follow up" if "cancel my subscription" in text.casefold() else "No phrase match")
```

**Preview a short recording before its final transcript is ready:** use the [Python](https://github.com/giggy-ai/giggy-python#stream-transcript-revisions-from-an-uploaded-wav) or [Node.js](https://github.com/giggy-ai/giggy-js#stream-transcript-revisions-from-an-uploaded-wav) Streaming example. Replace each provisional `transcript_chunk` with the next one, then verify the canonical result through the generation UUID. Streaming is paid.

## Developer resources

- Documentation: https://giggy.ai/docs/speech-api
- OpenAPI 3.1: https://giggy.ai/v1/openapi.json
- Official JavaScript/TypeScript SDK: https://github.com/giggy-ai/giggy-js
- MCP endpoint: https://giggy.ai/mcp
- Pricing: https://giggy.ai/pricing
- MCP setup repository: https://github.com/giggy-ai/giggy-mcp
- [Postman API Collection](postman/Giggy-Speech-API.postman_collection.json) — [Public Postman workspace](https://www.postman.com/giggy-ai/giggy-speech-api/collection/w1k6ylw/giggy-speech-api)
- [Free Batch TTS with Python](python/basic-tts/README.md)
- [Giggy vs ElevenLabs TTS Comparison](tutorials/02-giggy-vs-elevenlabs/README.md)

## Quick start

Set a Giggy API key and voice UUID:

```bash
export GIGGY_API_KEY="giggy_sk_..."
export GIGGY_VOICE_ID="your-giggy-voice-uuid"
```

Generate an MP3 with the native Giggy text-to-speech REST API:

```bash
curl --fail --show-error \
  --request POST "https://giggy.ai/v1/text-to-speech" \
  --header "xi-api-key: ${GIGGY_API_KEY}" \
  --header "content-type: application/json" \
  --header "idempotency-key: quickstart-$(date +%s)-$$" \
  --data "{\"text\":\"Hello from Giggy.\",\"voice_id\":\"${GIGGY_VOICE_ID}\",\"model_id\":\"giggyspeech\",\"mode\":\"batch\",\"output_format\":\"mp3_24000_160\",\"voice_settings\":{\"speed\":1}}" \
  --output speech.mp3
```

For framework-specific integrations, use the examples below.

## Core API endpoints

Native Giggy text-to-speech:

```text
POST https://giggy.ai/v1/text-to-speech
```

OpenAI-compatible text-to-speech:

```text
POST https://giggy.ai/v1/audio/speech
```

Available voices for your Giggy account:

```text
GET https://giggy.ai/v1/voices
```

This endpoint requires a bearer token. Use the `voice_id` field from each item in the returned `voices` array.

Public connector voice catalog:

```text
GET https://giggy.ai/v1/integrations/voices
```

Vapi custom TTS:

```text
POST https://giggy.ai/v1/integrations/vapi/text-to-speech/{voiceId}
```

MCP:

```text
https://giggy.ai/mcp
```

## Authentication

The native Giggy REST API uses:

```text
xi-api-key: $GIGGY_API_KEY
```

The OpenAI-compatible API, Vapi adapter, and MCP use:

```text
Authorization: Bearer $GIGGY_API_KEY
```

Keep Giggy API keys server-side.

## Environment

Set:

```bash
export GIGGY_API_KEY="giggy_sk_..."
export GIGGY_VOICE_ID="your-giggy-voice-uuid"
```

You can get a public voice UUID from:

```text
GET https://giggy.ai/v1/voices
```

## Examples

| Example | Directory |
| --- | --- |
| Native Node.js Batch TTS | [node/basic-tts/](node/basic-tts/) |
| Native Node.js Streaming TTS | [node/streaming-tts/](node/streaming-tts/) |
| OpenAI-compatible Node.js | [node/openai-compatible/](node/openai-compatible/) |
| Native Python Batch TTS | [python/basic-tts/](python/basic-tts/) |
| LiveKit Python | [livekit/python/](livekit/python/) |
| Pipecat Python | [pipecat/python/](pipecat/python/) |
| Vapi custom TTS | [vapi/](vapi/) |
| MCP | [mcp/](mcp/) |

## Node.js: Batch TTS

Run:

```bash
node node/basic-tts/index.mjs
```

The example writes:

```text
node/basic-tts/speech.mp3
```

Batch TTS uses Giggy's zero-credit Batch mode.

## Node.js: Streaming TTS

Run:

```bash
node node/streaming-tts/index.mjs
```

The example progressively writes raw:

```text
PCM16 little-endian
mono
24000 Hz
```

to:

```text
node/streaming-tts/speech.pcm
```

Streaming mode uses the applicable paid Giggy speech mode.

## OpenAI-compatible Node.js

Install:

```bash
cd node/openai-compatible
npm install
```

Run:

```bash
node index.mjs
```

The example uses the official OpenAI JavaScript client but points it at:

```text
https://giggy.ai/v1
```

No OpenAI API key is required. Use your Giggy API key.

## Python: Batch TTS

Run:

```bash
python python/basic-tts/main.py
```

This example uses `requests`; install it with `python -m pip install -r tutorials/requirements.txt`.

## LiveKit

See:

```text
livekit/python/README.md
```

Giggy works with LiveKit's OpenAI-compatible TTS plugin by setting a custom API base URL.

This is a compatibility integration, not a native Giggy provider listing in LiveKit.

## Pipecat

See:

```text
pipecat/python/README.md
```

The Pipecat example uses a small `TTSService` adapter because Pipecat's current built-in OpenAI TTS implementation validates voices against OpenAI's own named voice set before making a request.

Giggy voices use UUIDs.

This is a compatibility integration, not a native Giggy provider listing in Pipecat.

## Vapi

See:

```text
vapi/README.md
```

Giggy implements Vapi's custom TTS webhook contract.

This is a custom TTS integration, not a native Giggy provider listing in Vapi.

## MCP

See:

```text
mcp/README.md
```

and the dedicated repository:

```text
https://github.com/giggy-ai/giggy-mcp
```

## Pricing modes

Giggy currently exposes:

```text
batch
fast
streaming
```

Batch generation uses zero credits.

Fast, Streaming, OpenAI-compatible, Vapi, and other realtime compatibility paths use the applicable paid speech mode described in Giggy's current documentation.

Always use the live pricing page as the pricing source of truth:

```text
https://giggy.ai/pricing
```

## STT in voice-agent frameworks

Start with the complete [Python recording walkthrough](python/basic-tts/README.md#transcribe-a-recording) or [Node recording walkthrough](node/basic-tts/README.md#transcribe-a-recording). Both existing executables support Batch, Fast and uploaded-WAV Streaming; they log the admitted UUID, reconcile durable status, and save final text.

| Application | Existing path | STT responsibilities |
| --- | --- | --- |
| Archived meeting or phone call | Run the recording walkthrough on a locally converted WAV | Export authorized media, keep its UUID, protect the saved transcript; no speaker attribution or timestamps |
| Live captions | Use the Python microphone or Node PCM replay example in the SDK README | Read SSE concurrently with ordered PCM frames; replace provisional text and finish each input explicitly |
| LiveKit voice agent | Existing TTS example plus your chosen STT implementation | Keep API keys on the agent server; resample microphone PCM to 16 kHz; map cumulative transcript revisions; manage VAD, turns, interruption and audio playback in the agent |
| Pipecat voice agent | Existing [Giggy STT adapter](https://github.com/giggy-ai/pipecat-giggy#speech-to-text) plus the TTS example here | Follow that adapter's pinned requirements and readiness/frame contract; use its documented duration limits |
| Vapi phone agent | Existing custom TTS configuration; export completed call recordings for the recording walkthrough | Choose a supported Vapi transcriber separately. The custom TTS webhook does not make Giggy a native Vapi STT provider |

Giggy's public live input is a short session: PCM16 little-endian, mono, 16 kHz; 0.5–30 seconds total audio; finish within 35 seconds after microphone readiness. Read events while sending, wait for each frame acknowledgement, and never resend ambiguously accepted frames. The server does not end a turn merely because the speaker is silent. Long conversations need explicit application turn boundaries; this guide does not present a reconnection or automatic retry rail.

For an end-to-end STT → LLM → TTS example, the existing [Giggy voice-agent repository](https://github.com/giggy-ai/giggy-voice-agent) provides a separate server-side bridge with its own README and requirements. The core flow is recognition, a checked LLM reply, then speech synthesis. Do not send provisional text to actions that require a verified final transcript. Stop owned reply/playback work when your application's interruption detector fires.

### Migrating an AssemblyAI recording workflow

Convert the original audio/video/URL input locally to a compatible WAV. Replace the SDK transcription call with `transcriptions.transcribe` and consume the final `text`. For explicit control, map submit/status/result to `submit/get/result`; for live audio, use the Giggy readiness and ordered-frame contract rather than AssemblyAI WebSocket messages.

There are no direct Giggy request equivalents for speaker labels, word timestamps, confidence, chapters, sentiment, PII redaction or domain keyterm prompting. Remove those options rather than inventing fields. Any separate text-processing step belongs to your application and must be identified as such.

### Reproducing SDK verification

The Node SDK's existing `test/live-smoke.mjs` checks recorded Fast/SSE when GIGGY_STT_WAV is set; paid checks require GIGGY_RUN_PAID_SMOKE=1. Use an authorized test key and a short fixture with a known reference. Keep generation UUIDs and terminal statuses, never tokens or signed URLs. A successful TTS smoke is not evidence that STT works.

Provider contribution status and links are tracked in [upstream-submissions.md](docs/upstream-submissions.md). A fork, patch or submitted PR is different from an accepted provider shipped by the upstream framework.
