# Giggy Speech MCP on Postman

Open the [native MCP collection](https://www.postman.com/giggy-ai/giggy-speech-api/collection/6ace9f50d5652f476d274389) in the [Giggy workspace](https://www.postman.com/giggy-ai/giggy-speech-api/overview).

The saved **Connect to Giggy Speech MCP** request uses HTTP (Streamable HTTP), `https://giggy.ai/mcp`, and Bearer Token `{{GIGGY_API_KEY}}`. Set your key in a private environment and select it before connecting. No key is included in this repository or the public collection.

1. Connect and inspect the server's current tool schemas.
2. Call `list_voices` with `language: "English"`, `limit: 10`.
3. Use a returned `voice_id` in `generate_speech`; explicitly choose `mode: "batch"` for free queued speech. Use a fresh `idempotency_key` for each intended generation.
4. Retain `generation.generation_uuid`, then poll `get_speech_generation` until completed. Do not resubmit while queued or processing.
5. Fetch `generation.result.url` without attaching your Giggy API key. The signed result URL is private.

For recorded transcription, call `transcribe_audio` with an authorized WAV data URL (`data:audio/wav;base64,...`), `mode: "batch"`, and optionally `language: "English"`. WAV must be PCM16 LE mono 16 kHz, 0.5–60 seconds for Batch. Poll `get_speech_generation` for the completed transcript. The adjacent sample-recording.wav can be used for evaluation.

The server also exposes `list_my_voices`. MCP does not ingest live microphone frames. Use the [Python](https://github.com/giggy-ai/giggy-python) or [JavaScript SDK](https://github.com/giggy-ai/giggy-js) for live workflows. Fast and Streaming use prepaid credits; see [pricing](https://giggy.ai/pricing). STT does not provide diarization, word timestamps, sentiment, or PII redaction.

For Codex, Claude Code, Cursor and other client setup, see [giggy-mcp](https://github.com/giggy-ai/giggy-mcp). The native MCP request is maintained in Postman; it is separate from the REST v2.1 collection JSON.
