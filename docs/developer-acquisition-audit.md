# Developer acquisition implementation audit

Checked 2026-10-12 through live GitHub/registry APIs and clean source checkouts. No dashboards or customer analytics exports were accessed. No billable inference calls were made in this pass.

## Current state and implemented work

| Repository | Verified starting state | Implementation / decision |
| --- | --- | --- |
| giggy-ai/.github | Organization profile lists JS and compatibility examples; Python SDK and voice sandbox missing from primary path | Replace profile with a choose-your-path table, account/key/voice/first-audio steps and accurate community status. Repository descriptions/topics and six pins are review-only proposals in the profile PR. |
| giggy-js | Source version 0.1.1; npm latest 0.1.0; clear core request API and offline CI | Add direct account/docs/demo CTAs, PowerShell setup and source-versus-registry status. Existing 11 SDK tests pass; no speculative SDK feature expansion. |
| giggy-python | Version 0.1.0 in source; PyPI project JSON returns 404; automatic tag-triggered publication workflow | Add source-install/first-voice onboarding, first-speech example, redirect rejection, bounded/closed HTTP errors, PCM response checks, mode/speed validation and explicit SDK User-Agent. Manual owner-confirmed publishing and installed-wheel CI replace automatic tag publication. |
| giggy-examples | Multiple working compatibility examples; benchmark summary reads an ignored missing results.csv; historical multi-rate claims | Fix honest empty-baseline handling. Add read-only intent discovery in the existing discovery directory. Add Batch idempotency/redirect safety and offline tests. Correct Vapi and Pipecat rates to the current 24 kHz contract. Link existing demos rather than cloning them. |
| pipecat-giggy | Main/PyPI version 0.2.0; STT PR #3 merged. Demo PR #1 open; cloud sandbox #2 draft/open | Remove unverified marketing scope from onboarding and link existing demos. Refresh #2 against published STT/main, preserving source-install sandbox extras and server-issued streaming UUID support. No main merge or package publication. |
| giggy-mcp | Client configurations and registry/plugin status document exist | Add the durable first-speech success criterion, account/docs/demo links and real-time transport distinction. Existing registry document is historical evidence, not a new directory approval. |
| giggy-voice-agent | Main contains cloud-only BYOK demo; default Angela intro; 22 tests and credential scan pass | Keep existing app. Improve start/stop/disconnect success criteria, SDK/native-Pipecat routing and tagged CTAs. No new demo or unapproved live microphone call. |
| giggy-ai/agents fork | Native Giggy plugin branch and existing LiveKit PR #7659; not accepted/released | Prepare a follow-up branch with a gated first-WAV example and two offline tests. Existing provider tests plus follow-up total 34 passing. Do not update the upstream PR without approval. |
| giggy-ai/pipecat-docs fork | TTS docs #1450, setup links #1458 and STT docs #1468 merged upstream | Base the follow-up on current upstream main, add neutral links distinguishing Node sandbox from unmerged Pipecat demos. Prettier and Mint build validation pass. No third-party PR submitted. |

## Priority order

1. Review/merge the core onboarding and release-readiness PRs. The profile and examples give the highest immediate benefit without new products or repositories.
2. Review the refreshed native sandbox #2. Physical microphone and hosted browser checks remain before device-specific compatibility claims.
3. Owner approves the proposed repository descriptions/topics and pins; apply through existing settings only after that approval. No organization settings changed here.
4. Confirm Python package name ownership, Trusted Publishing and protected environment; authorize a release separately.
5. Review the two upstream follow-ups below and the existing LiveKit CLA status. Keep proposals accurate about maintenance and release ownership.
6. Obtain authorized weekly analytics exports. Do not infer API adoption from stars or issue matches.

## Two upstream contributions to prioritize

### LiveKit native provider onboarding

Reuse [LiveKit PR #7659](https://github.com/livekit/agents/pull/7659), currently open. The plugin already implements complete-text progressive 24 kHz PCM with UUID voices, cancellation cleanup and no automatic retries. Follow-up code adds a first-WAV example requiring explicit paid opt-in, plus synthetic-frame WAV/cleanup and no-opt-in/no-provider tests. Contribution guidelines require documented new methods, Ruff, strict typing, tests and CLA. No plugin versions or dependency floors are changed. Full workspace sync/check is not claimed; scoped tests use LiveKit 1.8.5. Owner resolves CLA/reviewer feedback before submitting any follow-up; live room/provider qualification remains separately authorized.

### Pipecat application discovery documentation

[Giggy TTS docs](https://github.com/pipecat-ai/docs/pull/1450), [setup/demo links](https://github.com/pipecat-ai/docs/pull/1458) and [STT docs](https://github.com/pipecat-ai/docs/pull/1468) are merged. Reuse their provider pages. The follow-up links the existing standalone Node sandbox and native Pipecat demo PRs, explicitly describing what is merged and which runtime each uses. It adds no duplicate service/demo. Current contribution guidelines require MDX frontmatter/navigation consistency, Prettier and Mint checks. Changed MDX formats correctly and Mint build validation passes. A full repository broken-links pass is not claimed. The upstream docs dependency tree reports existing vulnerabilities; no unrelated dependency migration was performed. Owner reviews the patch before third-party submission.

Vapi is a lower-priority inclusion proposal until real call/sample-rate qualification exists. Its platform contract accepts multiple rates, while Giggy's current public contract accepts 24 kHz only. OpenAI-compatible clients already have a working configuration example; do not create another native plugin merely for discoverability.

## Validation and limits

- JS SDK: 11 offline tests, build, npm installation/audit; published version checked separately.
- Python SDK: 11 source/installed-wheel tests, sdist/wheel build, twine check, wheel import/license/py.typed checks; source Ruff and compilation checks. CI covers 3.10–3.13, but only local Python 3.12 is claimed until remote checks pass.
- Examples: 2 Node request tests, 8 discovery/baseline tests, 1 Python Batch test, OpenAI JS install/syntax check, LiveKit and Pipecat construction/rate smoke checks.
- Voice sandbox: 22 tests, syntax checks and public credential-pattern scan.
- Native Pipecat sandbox: 42 STT protocol tests and 3 actual native pipeline tests with provider stand-ins after refreshing against main.
- LiveKit proposal: 34 offline provider/example tests; focused Ruff formatting/lint.
- All prepared public files were compared against 42 private environment credential values: zero matches. No values were printed.
- The intent CLI queried GitHub's official API and produced a ranked live report with disclosed caps/incomplete-search warnings. Rule matches still require human relevance review; no full coverage or purchase intent is claimed.

API GETs used for repository/registry/specification/search audit do not synthesize speech. No package was published, upstream PR submitted, service deployed, main branch merged, organization setting changed or third party contacted. Existing records, recordings and private service source were not copied into public code.

## Measurement and pin recommendation

[Measurement plan](acquisition-measurement.md) records existing page_view campaign handling, signup-start/attempt and API-key UI events, plus missing first-successful-external-speech attribution. [Weekly KPI template](weekly-kpis.csv) has no fabricated counts.

Recommend six pins, in order: **giggy-voice-agent**, **pipecat-giggy**, **giggy-examples**, **giggy-js**, **giggy-python**, **giggy-mcp**. Use integration/demo repositories first, retain both language SDKs and MCP, and avoid pinning contribution forks as though they were released Giggy frameworks.
