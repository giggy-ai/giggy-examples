import os
import runpy
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

EXAMPLE = Path(__file__).resolve().parents[1] / "python/basic-tts/main.py"


class PythonExampleTests(unittest.TestCase):
    def test_one_request_per_run_with_fresh_idempotency_and_no_redirects(self):
        response = Mock(headers={"Content-Type": "audio/mpeg"}, content=b"fake-audio")
        with TemporaryDirectory() as tmp:
            previous = os.getcwd()
            try:
                os.chdir(tmp)
                with (
                    patch.dict(
                        os.environ,
                        {"GIGGY_API_KEY": "offline-key", "GIGGY_VOICE_ID": "fake-uuid"},
                        clear=True,
                    ),
                    patch("requests.post", return_value=response) as post,
                ):
                    runpy.run_path(str(EXAMPLE))
                    runpy.run_path(str(EXAMPLE))
                self.assertEqual(post.call_count, 2)
                keys = [
                    call.kwargs["headers"]["Idempotency-Key"]
                    for call in post.call_args_list
                ]
                self.assertNotEqual(*keys)
                self.assertFalse(post.call_args.kwargs["allow_redirects"])
                self.assertEqual(Path("speech.mp3").read_bytes(), b"fake-audio")
            finally:
                os.chdir(previous)


if __name__ == "__main__":
    unittest.main()
