import csv
import json
import unittest
from datetime import date
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock
from urllib.error import HTTPError, URLError

import github_intent as tool


def issue(**changes):
    return {
        "html_url": "https://github.com/example/voice/issues/1",
        "state": "open",
        "title": "Looking for an ElevenLabs alternative",
        "body": "Need a TTS provider.",
        "created_at": "2026-10-01T00:00:00Z",
        "updated_at": "2026-10-12T00:00:00Z",
        **changes,
    }


class Response(BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class DiscoveryTests(unittest.TestCase):
    def test_rank_rules_and_exclude_unrelated(self):
        for title, level in [
            ("Recommend a TTS provider", "high"),
            ("TTS streaming timeout", "medium"),
            ("TTS demo notes", "low"),
        ]:
            row = tool.classify(
                issue(title=title, body=""), tool.DEFAULT_WEIGHTS, date(2026, 9, 1)
            )
            self.assertEqual(row["classification"], level)
            self.assertIn("Speech topic:", row["evidence"])
        self.assertIsNone(
            tool.classify(
                issue(title="Looking for a SQL provider", body=""),
                tool.DEFAULT_WEIGHTS,
                date(2026, 9, 1),
            )
        )

    def test_drop_closed_pr_old_and_external_urls(self):
        for change in [
            dict(state="closed"),
            dict(pull_request={}),
            dict(updated_at="2020-01-01"),
            dict(html_url="https://evil.test/issues/1"),
        ]:
            self.assertIsNone(
                tool.classify(issue(**change), tool.DEFAULT_WEIGHTS, date(2026, 9, 1))
            )

    def test_digest_and_distant_provider_requests_are_not_high_intent(self):
        self.assertIsNone(
            tool.classify(
                issue(title="Upstream sync: release notes"),
                tool.DEFAULT_WEIGHTS,
                date(2026, 9, 1),
            )
        )
        row = tool.classify(
            issue(title="TTS notes", body="x" * 300 + "Looking for an SQL provider"),
            tool.DEFAULT_WEIGHTS,
            date(2026, 9, 1),
        )
        self.assertEqual(row["classification"], "low")
        row = tool.classify(
            issue(
                title="TTS latency bug", body="Describe alternatives considered: none"
            ),
            tool.DEFAULT_WEIGHTS,
            date(2026, 9, 1),
        )
        self.assertEqual(row["classification"], "medium")

    def test_deduplicate_filter_and_custom_score(self):
        search = Mock(
            return_value={
                "items": [
                    issue(),
                    issue(
                        title="TTS notes",
                        body="",
                        html_url="https://github.com/example/voice/issues/2",
                    ),
                ],
                "total_count": 2,
            }
        )
        rows, warnings = tool.collect(
            ["TTS", '"ElevenLabs alternative"'],
            {"high": 95, "medium": 60, "low": 10},
            min_score=20,
            search=search,
            today=date(2026, 10, 12),
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["score"], 95)
        self.assertEqual(warnings, [])
        self.assertIn("is:public", search.call_args.args[0])
        self.assertIn("is:open", search.call_args.args[0])
        with self.assertRaises(tool.DiscoveryError):
            tool.collect(["TTS is:closed"], tool.DEFAULT_WEIGHTS, search=search)

    def test_pagination_caps_are_visible(self):
        search = Mock(
            return_value={
                "items": [issue()] * 50,
                "total_count": 200,
                "incomplete_results": True,
            }
        )
        rows, warnings = tool.collect(
            ["TTS"],
            tool.DEFAULT_WEIGHTS,
            pages=2,
            search=search,
            today=date(2026, 10, 12),
        )
        self.assertEqual(search.call_count, 2)
        self.assertEqual(len(rows), 1)
        self.assertEqual(len(warnings), 2)

    def test_rate_limits_bounded_and_errors_sanitized(self):
        limited = HTTPError(
            "url", 429, "private detail", {"Retry-After": "1"}, BytesIO(b"private body")
        )
        opener = Mock(
            side_effect=[limited, Response(json.dumps({"items": []}).encode())]
        )
        sleep = Mock()
        self.assertEqual(
            tool.search_page("TTS", 1, "secret", opener=opener, sleeper=sleep)["items"],
            [],
        )
        sleep.assert_called_once_with(1)
        request = opener.call_args.args[0]
        self.assertEqual(request.get_method(), "GET")
        self.assertEqual(request.host, "api.github.com")
        blocked = Mock(
            side_effect=HTTPError(
                "url",
                403,
                "secret",
                {"X-RateLimit-Remaining": "0", "Retry-After": "120"},
                BytesIO(),
            )
        )
        with self.assertRaisesRegex(tool.DiscoveryError, "rate limit"):
            tool.search_page("TTS", 1, "secret", opener=blocked, max_wait=0)
        with self.assertRaisesRegex(tool.DiscoveryError, "could not complete"):
            tool.search_page(
                "TTS", 1, "secret", opener=Mock(side_effect=URLError("secret"))
            )

    def test_reports_redact_contacts_and_neutralize_csv_formulas(self):
        row = tool.classify(
            issue(
                title="=TTS contact somebody@example.com +15551234567 "
                + "ghp_"
                + "x" * 30
                + " | <script>"
            ),
            tool.DEFAULT_WEIGHTS,
            date(2026, 9, 1),
        )
        with TemporaryDirectory() as tmp:
            tool.write_reports([row], [], Path(tmp), days=90)
            markdown = (Path(tmp) / "issues.md").read_text()
            self.assertNotIn("somebody@example.com", markdown)
            self.assertNotIn("<script>", markdown)
            self.assertNotIn("+15551234567", markdown)
            self.assertNotIn("ghp_" + "x" * 30, markdown)
            with (Path(tmp) / "issues.csv").open(newline="") as file:
                record = next(csv.DictReader(file))
            self.assertTrue(record["title"].startswith("'="))

    def test_secondary_limit_without_retry_header_and_permission_failure(self):
        limited = HTTPError(
            "url",
            403,
            "detail",
            {},
            BytesIO(b'{"message":"You have exceeded a secondary rate limit"}'),
        )
        sleep = Mock()
        opener = Mock(side_effect=[limited, Response(b'{"items":[]}')])
        self.assertEqual(
            tool.search_page("TTS", 1, None, opener=opener, sleeper=sleep),
            {"items": []},
        )
        sleep.assert_called_once_with(60)
        denied = Mock(
            side_effect=HTTPError(
                "url",
                403,
                "detail",
                {},
                BytesIO(b'{"message":"Resource not accessible"}'),
            )
        )
        with self.assertRaisesRegex(tool.DiscoveryError, "HTTP 403"):
            tool.search_page("TTS", 1, None, opener=denied, sleeper=sleep)
        self.assertEqual(denied.call_count, 1)


if __name__ == "__main__":
    unittest.main()
