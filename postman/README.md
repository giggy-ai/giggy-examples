# Giggy Postman examples

Import `Giggy-Speech-API.postman_collection.json` into Postman, or fork the [public workspace](https://www.postman.com/giggy-ai/giggy-speech-api/overview).

Set `GIGGY_API_KEY` in a private environment. Run **Find English voices**, then **Free Batch TTS**. Voice selection is populated from the API response. **Fast TTS (Paid)** is optional and uses credits.

For recorded transcription select `sample-recording.wav` in the binary body of **Transcribe recording — Free Batch**, then use **Check transcript status** and **Download completed transcript**. The sample is Giggy-generated speech: “Hello from Giggy. This is a short recording for speech transcription.” It is PCM16 LE, mono, 16 kHz and contains no private recording.

HTTP 202 is admission, not completion. Keep API keys and signed result URLs private. The signed download request intentionally has no API-key header. Batch recordings must be 0.5–60 seconds.

The separate [public MCP collection](https://www.postman.com/giggy-ai/giggy-speech-api/collection/6ace9f50d5652f476d274389) connects to `https://giggy.ai/mcp` with your own Bearer API key. It documents `list_voices`, `list_my_voices`, `generate_speech`, `transcribe_audio`, and `get_speech_generation`. See [Giggy MCP setup](https://github.com/giggy-ai/giggy-mcp). MCP handles completed recordings, not live microphone frames.
