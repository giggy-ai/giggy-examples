# Giggy upstream ecosystem submissions

| Ecosystem | Artifact | Status | External URL | Verification |
| --- | --- | --- | --- | --- |
| LiveKit | Native TTS provider plus compatibility documentation | PR open; not merged/released | https://github.com/livekit/agents/pull/7659 | Reviewed October 13: offline package/type checks documented; real synthesis/room tests and CLA signature remain pending. The contribution does not provide STT. |
| Pipecat | Giggy-maintained TTS/live STT adapter | Published pipecat-giggy 0.2.0; upstream listing acceptance not established | https://pypi.org/project/pipecat-giggy/0.2.0/ | Python 3.11+, Pipecat 1.12.0. The package README and existing live replay test define the STT contract. Provider publication is separate from upstream inclusion. |
| Vapi | Custom TTS documentation | Not submitted | — | No verified contribution channel or authorized Vapi test call. |

Package and PR status was checked on October 13, 2026. No upstream acceptance is claimed. Follow the linked source/release instructions and distinguish offline tests, real API replay, live-room/call qualification and upstream acceptance. A CLA is a legal agreement for the human contributor to review and sign.

## Developer discovery documentation update — October 13, 2026

The existing SDK and examples READMEs now lead with STT as well as TTS, link each transcription workflow, and explain endpoint-specific OpenAI migration. This is documentation-only: no endpoint, request/response field, authentication, billing, SDK method or adapter implementation changes. README edits are local until explicitly published. Repository summaries/topics and upstream listing acceptance are separate from source publication.

| Repository | Description | Additive discovery topics |
| --- | --- | --- |
| giggy-python | Official Python SDK for Giggy text-to-speech and speech-to-text APIs, including recording and short live microphone transcription. | speech-to-text, stt, asr, transcription |
| giggy-js | Official JavaScript and TypeScript SDK for Giggy text-to-speech and speech-to-text APIs, including recording and short live PCM transcription. | speech-to-text, stt, asr, transcription, typescript |
| giggy-examples | Runnable Python and JavaScript examples for Giggy STT and TTS APIs, recording transcription, live PCM and voice-framework integrations. | speech-to-text, stt, transcription, text-to-speech, voice-agents |
| pipecat-giggy | Giggy-maintained text-to-speech and live speech-to-text integration for Pipecat voice agents. | speech-to-text, stt, transcription, text-to-speech, pipecat |

The four descriptions and additive topics above were saved and verified in GitHub's repository metadata UI on October 13. Existing topics and website links were preserved; the Pipecat repository's previously empty website now links to the STT developer guide. Evidence is in the project's approved `z_temp_testing/developer-discovery-github-metadata.json` and repository screenshots. These metadata edits do not publish the local README changes or release packages.

Preserve existing relevant topics. Do not label all STT as OpenAI-compatible. The OpenAI compatibility path here is TTS; uploaded recording STT uses raw WAV and asynchronous admission or cumulative SSE, while live input uses readiness and acknowledged ordered PCM frames.

## Prepared Pipecat listing description

**Title:** Giggy text-to-speech and live speech-to-text integration

Giggy maintains `pipecat-giggy`, a Pipecat integration providing streaming TTS and live STT. The existing 0.2.0 adapter targets Pipecat 1.12.0. TTS uses a Giggy voice UUID; STT accepts PCM16 mono 16 kHz audio and does not require a voice UUID. Applications supply transport, VAD, turn boundaries and resampling. Each live STT operation accepts 0.5–30 seconds of audio and must finish input within 35 seconds after readiness. Cumulative provisional transcripts replace earlier previews; final frames are emitted only after durable completion and canonical transcript retrieval.

Resources: [package](https://pypi.org/project/pipecat-giggy/0.2.0/), [maintained source and examples](https://github.com/giggy-ai/pipecat-giggy), [STT setup](https://giggy.ai/docs/speech-api#api-stt-developer-path), [pricing](https://giggy.ai/pricing). TTS and live STT are paid; free queued Batch is a separate recording API. No speaker diarization, word timestamps, guaranteed latency or native upstream acceptance is claimed. The recording replay exercises the live protocol and does not establish physical microphone or telephone qualification.

This text is prepared for maintainer review, not submitted. Recheck current contribution requirements and the existing adapter's verification receipts before submitting; do not create a second native provider implementation to obtain a listing.

## Remaining distribution work

- Pipecat: identify its current community integration listing process and supply the prepared description plus existing test evidence. Record an accepted URL only after maintainer confirmation.
- LiveKit: continue the existing TTS PR rather than opening a duplicate. Its TTS plugin does not establish STT support; the CLA remains a human signing step.
- n8n: use the existing node's TTS/voice-discovery capabilities and `examples/generate-voiceover.json`; it is not a recording-transcription node. Package 0.1.0 is published, while verified-node/Cloud acceptance is unconfirmed. Prepare its existing repository, package/version, installation instructions and production test evidence for the Creator Portal review. Do not claim verification before acceptance.
- Vapi: limit the listing proposal to the existing custom TTS webhook. Do not advertise Giggy as a native Vapi STT provider.

## Discovery rollout and measurement

Local documentation now provides a task-based tool chooser in the existing Speech API guide, examples README and GitHub profile; SDK/adapter READMEs link back to it. Existing MCP listing descriptions and skill instructions now cover recorded STT alongside TTS. These edits require source publication; updated registry README content requires a separately authorised package release. No API/playground implementation or retry policy is changed.

Before promoting the LiveKit example for paid workloads, resolve or explicitly review its default retry risk recorded in the production audit. Browser/microphone, room and phone qualification remain separate gates. Maintain listing status here and in MCP submission notes; do not create duplicate provider implementations or treat pending approvals as accepted.

Use the [existing discovery benchmark](../discovery/README.md) and existing analytics for baseline/post-publication comparisons. No new analytics schema, automated schedule, outreach or external submission is introduced by this documentation pass.

No outreach, upstream PR submission, legal agreement, package release, runtime change or production deployment is included in this documentation update.
