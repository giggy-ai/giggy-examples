# Read-only GitHub technical-needs discovery

Search public open issues through GitHub's official REST API. This standard-library Python 3.10+ CLI does not require an LLM, paid inference, `gh`, or a Giggy API key. It belongs alongside the existing discoverability benchmark; it does not replace or fabricate benchmark results.

```sh
python discovery/github_intent.py --config discovery/github-intent.example.json --days 90 --output discovery/runs/latest
python -m unittest discover -s discovery -p test_github_intent.py -v
```

Optionally set `GITHUB_TOKEN` or `GH_TOKEN` to a token with public read access. If neither is set and `gh` is installed, the CLI reads `gh auth token`. Tokens are used only in the authorization header to `api.github.com`; never printed or saved in reports. Unauthenticated searches also work within GitHub's lower rate limits.

Use repeated `--query` arguments to replace default themes, or edit the JSON config's queries and weights. The CLI enforces `is:issue is:open is:public` and a recent `updated` cutoff. Reports contain both creation and update dates: an older issue with recent technical discussion may qualify. `--pages 1` retrieves at most 50 items per query; use up to five pages or narrower queries. Results are deduplicated by URL; incomplete searches and capped result counts are disclosed. No exhaustive coverage is claimed.

Rules require a TTS/speech-synthesis topic. Explicit requests for alternatives, recommendations or integration receive High/90; technical failures or integration needs Medium/60; general speech discussions Low/20. Configure scores and use `--min-score 60` to keep only higher-relevance results. Automated digests and trend titles are excluded; stated needs must occur near a speech topic. Keyword rules can still misclassify quoted or resolved discussion: scores are review priorities, not verified purchase intent. Evidence records matched technical phrases, not author profiles or full issue bodies. Reports exclude authors and contact details, redact contact strings in titles, escape Markdown and neutralize CSV formulas.

Outputs are `issues.md` and `issues.csv`, with repository, issue URL, title, dates, score/classification, evidence and a recommended technical contribution. Empty results are reported honestly. The CLI never comments, mentions, messages, stars, emails, harvests contacts or generates promotional replies. A human must confirm the issue is still open, reproduce the technical need, read contribution guidelines and approve any proposed contribution. Follow [GitHub's Acceptable Use Policies](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies).

## Rate limits and optional reporting

HTTP 429 and rate-limit HTTP 403 honor `Retry-After` or the reset header, with at most two retries. The default maximum wait is 60 seconds per retry; longer limits stop with a sanitized message. `--max-wait 0` fails promptly. Permission failures do not retry. Existing reports remain intact on failed searches.

The `GitHub issue research` Actions workflow is manually dispatched and uploads a seven-day report artifact with read-only permissions. It is not scheduled by default. To opt into weekly reporting, review the query scope and add `schedule: [{cron: '0 9 * * 1'}]` alongside `workflow_dispatch`. Scheduled reports still perform only GET searches and artifact uploadsâ€”no issues, comments, messages or automated promotion. Reduce frequency/query volume if GitHub asks you to. Retain reports only as long as needed for technical review.
