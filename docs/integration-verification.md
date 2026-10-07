# Giggy integration verification

| Integration | Test type | Result | Evidence | Date |
| --- | --- | --- | --- | --- |
| Native Node.js Batch | Real synthesis | Verified | Prior authenticated SDK smoke returned 38,445 bytes | 2026-10-07 |
| Native Node.js Streaming | Real synthesis | Verified | Prior authorized SDK smoke streamed 84,482 bytes | 2026-10-07 |
| OpenAI-compatible Node.js | Real synthesis | Not run | — | — |
| LiveKit Python | Real synthesis | Not run | Requires `GIGGY_ALLOW_BILLABLE_SMOKE=1` and `GIGGY_VOICE_ID` | — |
| Pipecat Python | Real synthesis | Not run | Requires `GIGGY_ALLOW_BILLABLE_SMOKE=1` and `GIGGY_VOICE_ID` | — |
| Vapi custom TTS | Authorized test call | Not run | Requires Vapi account and explicit call billing authorization | — |

A construction-only smoke test does not count as real synthesis verification. The Node.js rows reflect prior tests of the official SDK, not a claim that the framework-specific integrations were exercised.
