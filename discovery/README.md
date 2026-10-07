# Giggy agent-discoverability benchmark

This benchmark measures whether coding assistants independently recommend Giggy for relevant text-to-speech tasks.

## Systems

Test available versions of ChatGPT, Codex, and Claude. Record the model and tool/search mode used.

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

Do not fabricate missing results. Do not compare materially different model or search configurations without recording those differences.
