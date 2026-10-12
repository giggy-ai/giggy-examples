# GitHub acquisition measurement

GitHub discovery → repository/docs visit → Giggy signup → API key created → first successful speech generation.

Status is based on source inspection on 2026-10-12, not dashboards or measured conversion counts.

| Stage | Available evidence | Limit / work required |
| --- | --- | --- |
| Discovery | Read-only issue reports and upstream PR status | Count human-qualified technical needs separately from keyword matches. |
| Repository visit | GitHub Traffic views/unique visitors/clones if an owner exports them | No export retrieved. Export weekly; stars do not measure API adoption. |
| Docs visit | Existing consent-gated GA page_view preserves campaign parameters | Tagged links added; actual delivery/property reports unverified. Same-path deduplication can omit repeated campaign visits. |
| Signup | UI signup_started/signup_attempted and backend completion state | Attempts are not completed signups. Verify completion export/event and attribution with the owner. |
| API key | Existing UI api_key_created | No verified report; does not establish a first API call or cover all creation surfaces. |
| First speech | Existing durable generation completion/first-output telemetry | First-per-account external speech aggregation and attribution are not implemented or verified here. |

No production service or schema was changed. No new event is claimed as deployed. Cross-device signup, key and REST-generation attribution need an owner-reviewed design using existing authorized records and consent controls. Never place keys, prompts, audio, contact details or raw private principal identifiers in GitHub reports. Exclude failures, retries/duplicates and internal demos from successful-user counts.

## Tagged links

Owned README CTAs use utm_source=github, utm_medium=referral, utm_campaign=developer_onboarding and utm_content=<repository>_readme or _docs. Tags belong on website links, not API endpoints, credentials or artifact URLs. Existing Pipecat campaign links remain comparable. Upstream proposals use neutral technical links rather than acquisition pitches.

## Weekly review

Copy [weekly-kpis.csv](weekly-kpis.csv); leave unavailable values empty/NA. Record date range, source, export time and limitations. Never fabricate missing counts or fill unknown analytics with zeros.

- Human-qualified opportunities: verify evidence and a useful reproduction, adapter or documentation fix. Do not measure promotional engagement.
- Upstream outcomes: proposed, submitted with approval, changes requested, accepted, released. Accepted docs are distinct from released code.
- Onboarding: clean installs and successful example runs, broken instructions, sanitized setup errors. Offline tests are not user conversions.
- Conversion: attributed visits → completed signups → key creation → first completed external speech. Report percentages only with known, compatible numerators, denominators, attribution and windows.

The first weekly report remains a template until owner-authorized GitHub Traffic and Giggy analytics exports are available.
