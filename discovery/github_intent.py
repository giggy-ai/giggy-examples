"""Read-only GitHub issue discovery. No engagement or personal-contact collection."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
from datetime import date, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_QUERIES = [
    '"ElevenLabs" "alternative"',
    '"TTS provider"',
    '"custom TTS"',
    '"speech latency"',
    '"OpenAI compatible" "TTS"',
    '"voice agent" "text to speech"',
    "repo:pipecat-ai/pipecat TTS",
    "repo:livekit/agents TTS",
]
DEFAULT_WEIGHTS = {"high": 90, "medium": 60, "low": 20}
SPEECH = re.compile(r"\b(tts|text[- ]to[- ]speech|speech synthesis|elevenlabs)\b", re.I)
HIGH = re.compile(
    r"\b(?:looking for|seeking|recommend(?:ation|ations)?|which provider).{0,80}\b(?:tts|speech|elevenlabs|provider)\b"
    r"|\b(?:tts|elevenlabs|speech synthesis).{0,40}\b(?:alternatives?|recommendations?)\b"
    r"|\balternatives?\s+(?:to|for)\s+(?:elevenlabs|tts|speech)\b"
    r"|\b(?:add|integrate|support).{0,40}\b(?:tts provider|custom tts|speech provider)\b",
    re.I,
)
PROBLEM = re.compile(
    r"\b(error|fail(?:s|ed|ure)?|bug|latency|timeout|custom tts|integration|streaming|interrupt(?:ion)?|compatible)\b",
    re.I,
)
CONTACT = re.compile(
    r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|(?:https?://)?(?:www\.)?(?:linkedin\.com/in|t\.me)/\S+",
    re.I,
)
SECRET = re.compile(r"\b(?:giggy_sk_|ghp_|github_pat_|sk-)[A-Za-z0-9_-]{16,}")
PHONE = re.compile(r"(?<!\w)\+\d[\d ()-]{7,}\d(?!\w)")
NOISE = re.compile(
    r"upstream sync|open source trends|daily digest|weekly roundup|日报|生态日报|release notes|changelog",
    re.I,
)
FIELDS = [
    "repository",
    "url",
    "title",
    "created_at",
    "updated_at",
    "classification",
    "score",
    "evidence",
    "recommended_contribution",
]


class DiscoveryError(Exception):
    """Sanitized API/configuration failure safe to show in a report."""


def redact(value):
    return SECRET.sub(
        "[credential redacted]",
        PHONE.sub("[contact redacted]", CONTACT.sub("[contact redacted]", value)),
    )


def token_from_environment() -> str | None:
    token = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
    if token:
        return token
    try:
        result = subprocess.run(
            ["gh", "auth", "token"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def search_page(
    query: str,
    page: int,
    token: str | None,
    *,
    opener=urlopen,
    sleeper=time.sleep,
    max_wait=60,
) -> dict:
    """Use only GET on the official API, with bounded rate-limit retries."""
    url = "https://api.github.com/search/issues?" + urlencode(
        {"q": query, "sort": "updated", "order": "desc", "per_page": 50, "page": page}
    )
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "giggy-issue-research/1.0",
    }
    if token:
        headers["Authorization"] = "Bearer " + token
    for attempt in range(3):
        try:
            with opener(
                Request(url, headers=headers, method="GET"), timeout=30
            ) as response:
                raw = response.read(8 * 1024 * 1024 + 1)
                if len(raw) > 8 * 1024 * 1024:
                    raise DiscoveryError("GitHub response exceeded the size limit.")
                data = json.loads(raw)
                if not isinstance(data, dict) or not isinstance(
                    data.get("items"), list
                ):
                    raise DiscoveryError("GitHub returned an invalid search response.")
                return data
        except HTTPError as error:
            retry = error.headers.get("Retry-After")
            limited = error.code == 429 or (
                error.code == 403
                and (
                    retry is not None
                    or error.headers.get("X-RateLimit-Remaining") == "0"
                )
            )
            if error.code == 403 and not limited:
                try:
                    message = str(json.loads(error.read(4096)).get("message", ""))
                    limited = "rate limit" in message.lower()
                except (ValueError, OSError, AttributeError):
                    pass
            try:
                reset = error.headers.get("X-RateLimit-Reset")
                delay = (
                    float(retry)
                    if retry is not None
                    else max(1, float(reset) - time.time() + 1)
                    if reset
                    else 60
                )
            except ValueError:
                delay = 60
            error.close()
            if limited and attempt < 2 and 0 <= delay <= max_wait:
                sleeper(max(1, delay))
                continue
            if limited:
                raise DiscoveryError(
                    "GitHub rate limit reached; rerun later or increase --max-wait."
                ) from None
            raise DiscoveryError(
                f"GitHub search returned HTTP {error.code}; check API access and query syntax."
            ) from None
        except (URLError, TimeoutError, json.JSONDecodeError):
            raise DiscoveryError(
                "GitHub search could not complete; no credentials or response bodies were logged."
            ) from None
    raise DiscoveryError("Search retry limit reached.")


def classify(issue: dict, weights: dict, cutoff: date) -> dict | None:
    """Keep only open public issue URLs and return non-contact technical evidence."""
    url = issue.get("html_url", "")
    match = re.fullmatch(r"https://github\.com/([\w.-]+/[\w.-]+)/issues/\d+", url)
    if not match or issue.get("state") != "open" or "pull_request" in issue:
        return None
    updated = str(issue.get("updated_at", ""))
    if updated[:10] < cutoff.isoformat():
        return None
    title = str(issue.get("title", ""))
    if NOISE.search(title):
        return None
    text = title + "\n" + str(issue.get("body") or "")
    speech = SPEECH.search(text)
    if not speech:
        return None
    # A request for an unrelated LLM provider elsewhere in a long issue must not
    # promote an incidental TTS mention to a qualified speech need.
    contexts = [
        text[max(0, m.start() - 100) : m.end() + 100] for m in SPEECH.finditer(text)
    ]
    focused = "\n".join(contexts)
    high, problem = HIGH.search(focused), PROBLEM.search(focused)
    level = "high" if high else "medium" if problem else "low"
    evidence = f"Speech topic: {speech.group().lower()}"
    if high:
        evidence += "; stated need: explicit speech-provider request pattern"
    elif problem:
        evidence += "; technical signal: " + problem.group().lower()
    if level == "high":
        action = "Review requested constraints; offer a tested minimal provider adapter or neutral comparison only if relevant."
    elif level == "medium":
        action = "Reproduce the failure; prepare a regression test or documented configuration fix for human review."
    else:
        action = "Read for context; no engagement suggested without a concrete technical need."
    return {
        "repository": match[1],
        "url": url,
        "title": redact(str(issue.get("title", "")))[:250],
        "created_at": str(issue.get("created_at", "")),
        "updated_at": updated,
        "classification": level,
        "score": weights[level],
        "evidence": redact(evidence),
        "recommended_contribution": action,
    }


def collect(
    queries,
    weights,
    *,
    days=90,
    pages=1,
    min_score=20,
    token=None,
    search=search_page,
    max_wait=60,
    today=None,
):
    cutoff = (today or date.today()) - timedelta(days=days)
    rows, warnings = {}, []
    for raw in queries:
        if not isinstance(raw, str) or not raw.strip() or len(raw) > 256:
            raise DiscoveryError(
                "Queries must be nonempty strings of at most 256 characters."
            )
        if re.search(r"(?:^|\s)(?:-?is:|state:|updated:|created:|visibility:)", raw):
            raise DiscoveryError(
                "Queries must omit state, visibility and date qualifiers; the CLI owns these filters."
            )
        query = f"{raw} is:issue is:open is:public updated:>={cutoff.isoformat()}"
        for page in range(1, pages + 1):
            data = search(query, page, token, max_wait=max_wait)
            if data.get("incomplete_results"):
                warnings.append(f"Incomplete search: {raw}")
            for issue in data["items"]:
                row = classify(issue, weights, cutoff)
                if row and row["score"] >= min_score:
                    rows[row["url"]] = row
            if len(data["items"]) < 50:
                break
        if data.get("total_count", 0) > pages * 50:
            warnings.append(
                f"Result cap reached: {raw}; narrow the query or increase --pages."
            )
    return sorted(rows.values(), key=lambda r: (-r["score"], r["url"])), sorted(
        set(warnings)
    )


def cell(value):
    text = str(value).replace("\r", " ").replace("\n", " ")
    return "'" + text if text.lstrip().startswith(("=", "+", "-", "@")) else text


def write_reports(rows, warnings, directory, *, days):
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "issues.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows({k: cell(row[k]) for k in FIELDS} for row in rows)

    def md(value):
        return (
            str(value)
            .replace("\n", " ")
            .replace("\r", " ")
            .replace("|", "\\|")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    lines = [
        "# Public GitHub technical needs",
        "",
        f"Generated {date.today().isoformat()}; open issues updated in the last {days} days. {len(rows)} qualified results.",
        "",
        "Rules classify stated technical needs, not purchase intent. A human must verify relevance, current issue state and maintainer guidelines before contributing. No comments or messages are sent. No author/contact profiles are collected.",
        "",
        "| Repository / issue | Title | Created / updated | Level / score | Evidence | Technical contribution |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| [{row['repository']}]({row['url']}) | {md(row['title'])} | {md(row['created_at'][:10])} / {md(row['updated_at'][:10])} | {row['classification']} / {row['score']} | {md(row['evidence'])} | {md(row['recommended_contribution'])} |"
        )
    if warnings:
        lines += ["", "Coverage limits", "", *["- " + md(w) for w in warnings]]
    (directory / "issues.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path)
    parser.add_argument(
        "--query", action="append", help="Repeat to replace default queries."
    )
    parser.add_argument("--days", type=int, default=90)
    parser.add_argument("--pages", type=int, choices=range(1, 6), default=1)
    parser.add_argument("--min-score", type=int, default=20)
    parser.add_argument(
        "--max-wait",
        type=int,
        default=60,
        help="Maximum seconds per bounded rate-limit retry.",
    )
    parser.add_argument("--output", type=Path, default=Path("discovery/runs/latest"))
    args = parser.parse_args(argv)
    try:
        config = (
            json.loads(args.config.read_text(encoding="utf-8")) if args.config else {}
        )
        queries = args.query or config.get("queries", DEFAULT_QUERIES)
        weights = {**DEFAULT_WEIGHTS, **config.get("weights", {})}
        if (
            not isinstance(queries, list)
            or not 1 <= len(queries) <= 20
            or not 1 <= args.days <= 365
            or not 0 <= args.max_wait <= 300
        ):
            raise DiscoveryError(
                "Use 1–20 queries, 1–365 days and a maximum wait of 0–300 seconds."
            )
        if any(
            type(weights.get(k)) is not int or not 0 <= weights[k] <= 100
            for k in DEFAULT_WEIGHTS
        ):
            raise DiscoveryError(
                "Classification weights must be integers from 0 to 100."
            )
        rows, warnings = collect(
            queries,
            weights,
            days=args.days,
            pages=args.pages,
            min_score=args.min_score,
            token=token_from_environment(),
            max_wait=args.max_wait,
        )
        write_reports(rows, warnings, args.output, days=args.days)
        print(
            f"Wrote {len(rows)} ranked issues to {args.output}. {len(warnings)} coverage warnings. No engagement performed."
        )
        return 0
    except (DiscoveryError, OSError, ValueError, TypeError, AttributeError) as error:
        print(
            str(error)
            if isinstance(error, DiscoveryError)
            else "Invalid configuration or report output path.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
