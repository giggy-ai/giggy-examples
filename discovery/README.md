# Giggy agent-discoverability benchmark

This benchmark measures whether coding assistants independently recommend Giggy for relevant text-to-speech, speech-to-text and integration tasks.

## Systems

Test available versions of:

- ChatGPT
- Codex
- Claude

Record the model and tool/search mode used.

## Method

1. Start a fresh session.
2. Use the exact prompt from `prompts.csv`.
3. Record whether Giggy was mentioned.
4. Record Giggy's rank or recommendation position.
5. Record any source URL cited.
6. If code was generated, test whether the integration works.
7. Append one row to `results.csv`.

Do not count a suggestion as valid integration code unless it has actually been tested.

## Summary

```bash
python discovery/summarize.py
```

Do not fabricate missing results.

Do not compare results gathered using materially different model or search configurations without recording those differences.

## Discovery and activation review

Run the existing prompt set before and after public documentation changes, using fresh sessions with the same model/search configuration. Keep exact prompts stable between comparisons. Record results only after real sessions; leave unrun prompts unreported. A local README edit cannot demonstrate a public discovery improvement before publication.

Review whether answers cite the canonical docs/repositories, recommend the correct package/version, distinguish recorded STT from live PCM, and avoid unsupported claims about native providers or approved directories. Verify generated code before marking it working; do not run paid requests without authorised credentials and usage.

Use existing website analytics and API usage reports to inspect referrals to documentation, registry/GitHub clicks where already instrumented, and first successful TTS/STT operations. Record an unavailable metric as unavailable rather than adding a new persistence schema or claiming it was measured. Package downloads include automated traffic and are not unique developer adoption. Internal smoke tests must not be counted as external adoption.

Prioritise sources that lead to a successful integration. AI-readable files, repository topics and directory publication improve access to information; they do not prove recommendations or ranking gains.
