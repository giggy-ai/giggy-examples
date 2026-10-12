import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import summarize


class SummaryTests(unittest.TestCase):
    def test_missing_or_empty_measurements_are_not_fabricated(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "results.csv"
            for exists in [False, True]:
                if exists:
                    path.write_text(
                        "agent,giggy_mentioned,cited_url,generated_code_passed\n"
                    )
                output = StringIO()
                with (
                    patch.object(summarize, "RESULTS_PATH", path),
                    redirect_stdout(output),
                ):
                    summarize.main()
                self.assertEqual(
                    output.getvalue().strip(), "No discovery measurements recorded."
                )


if __name__ == "__main__":
    unittest.main()
