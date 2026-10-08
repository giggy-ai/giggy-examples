# Free Text-to-Speech API with Python — Giggy Batch

Generate speech with Giggy's free Batch API and save the completed MP3 as `speech.mp3`. Requires Python 3.10+ and `requests`.

Sign in at [Giggy](https://giggy.ai). Open Speech API → API Keys and create an API key. In the Speech API Playground, select an available voice and copy its `voice_id` UUID from the generated request preview. Keep your API key private.

Execute these commands from the repository root:

```bash
python -m pip install -r tutorials/requirements.txt

export GIGGY_API_KEY="YOUR_API_KEY"
export GIGGY_VOICE_ID="YOUR_VOICE_UUID"

python python/basic-tts/main.py
```

Open `speech.mp3` from the current working directory in an MP3 player. The request uses `POST https://giggy.ai/v1/text-to-speech`, `model_id=giggyspeech`, `mode=batch`, `output_format=mp3_24000_160`, and `voice_settings.speed=1`, authenticated with the `xi-api-key` header.

Batch uses zero credits but is queued and subject to request-size limits and rate limits. The HTTP request waits for completed audio; no job polling is required. This example allows 600 seconds per request and stops on an HTTP error, timeout, or non-audio response.

[Giggy](https://giggy.ai) · [Speech API documentation](https://giggy.ai/docs/speech-api)
