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

## Transcribe a recording

This same executable also supports STT. Install the official Python SDK (`python -m pip install giggy==0.1.0` after its first PyPI release, or install the SDK source checkout). Only STT mode imports that SDK; the existing TTS mode continues to use requests.

1. Export a recording you are authorized to process. Keep the original private.
2. Convert it with FFmpeg: `ffmpeg -i call.mp3 -ac 1 -ar 16000 -c:a pcm_s16le recording.wav`.
3. Verify the format: `ffprobe -v error -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 recording.wav`. Expect pcm_s16le, 16000 and 1.
4. Set GIGGY_API_KEY in this server process and run from the repository root:

```bash
python python/basic-tts/main.py --stt recording.wav --mode batch --output transcript.txt
```

Batch is free for recordings lasting 0.5–60 seconds. For longer call recordings, select `--mode fast` (paid; up to 12 hours). For a provisional transcript during processing, use `--mode streaming` (paid). Preview lines go to stderr; stdout and the optional output file contain only the final transcript.

The program logs the generation UUID, polls durable status with a bounded deadline, fetches the signed transcript with no forwarded API key, and exits on failure. Keep that UUID for support or reconciliation after interruption. It never automatically repeats the upload. Existing retention/deletion rules govern the result; saving transcript.txt creates a separate copy that your application must protect and delete according to its own policy.

For a call-recording review, read transcript.txt and search a known phrase. A phrase match does not identify the speaker, classify sentiment or establish that an action actually occurred. This workflow transcribes an exported recording; it does not provision a phone number or connect to a telephone provider.

Troubleshooting: a 401/403 requires correcting the key/owning space; a 429 is a rejected admission; a timeout after a UUID requires reading that existing generation. An expired/deleted result cannot be recovered by polling. See the [SDK reference](https://github.com/giggy-ai/giggy-python#transcription-method-reference).
