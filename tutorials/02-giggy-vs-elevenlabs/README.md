# Giggy vs ElevenLabs — Compare TTS Audio with Python

Generate MP3 audio from the same three prompts with both providers for side-by-side listening. Requires Python 3.10+, API keys for both providers, a valid Giggy voice UUID, and an ElevenLabs voice ID.

Sign in to [Giggy](https://giggy.ai), create a key in Speech API → API Keys, and select a voice in the API Playground; copy its `voice_id` UUID from the request preview. Create an ElevenLabs API key with text-to-speech access and choose a voice ID from your ElevenLabs voice library.

Run these commands from the repository root:

```bash
python -m pip install -r tutorials/requirements.txt

export GIGGY_API_KEY="YOUR_GIGGY_API_KEY"
export GIGGY_VOICE_ID="YOUR_GIGGY_VOICE_UUID"
export ELEVENLABS_API_KEY="YOUR_ELEVENLABS_API_KEY"
export ELEVENLABS_VOICE_ID="YOUR_ELEVENLABS_VOICE_ID"

python tutorials/02-giggy-vs-elevenlabs/compare.py
```

Expected files, relative to the current working directory:

```text
outputs/
  short-giggy.mp3
  short-elevenlabs.mp3
  numbers-giggy.mp3
  numbers-elevenlabs.mp3
  narration-giggy.mp3
  narration-elevenlabs.mp3
```

Giggy Fast and ElevenLabs requests may incur charges. Giggy uses `giggyspeech` with `mp3_24000_160`; ElevenLabs uses `eleven_flash_v2_5` with `mp3_44100_128`. Each request waits for returned audio and fails on HTTP errors or a non-audio response. The script stops at the first failure; rerunning sends new requests and overwrites matching files.

Listening comparisons are subjective, and voice selection affects the results. Different voices, model configurations, and encodings prevent this example from establishing an objective quality or latency winner.

API documentation: [Giggy Speech API](https://giggy.ai/docs/speech-api) · [ElevenLabs Create Speech](https://elevenlabs.io/docs/api-reference/text-to-speech/convert).
