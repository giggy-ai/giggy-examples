import json
import os
import urllib.error
import urllib.request
import uuid
from pathlib import Path


API_URL = r"""https://giggy.ai/v1/text-to-speech"""
OUTPUT_PATH = Path(r"""speech.mp3""")


def main() -> None:
    api_key = os.environ.get(r"""GIGGY_API_KEY""")
    voice_id = os.environ.get(r"""GIGGY_VOICE_ID""")

    if not api_key:
        raise RuntimeError(
            r"""Set GIGGY_API_KEY before running this example."""
        )

    if not voice_id:
        raise RuntimeError(
            r"""Set GIGGY_VOICE_ID before running this example."""
        )

    payload = {
        r"""text""": r"""Hello from Giggy.""",
        r"""voice_id""": voice_id,
        r"""model_id""": r"""giggyspeech""",
        r"""mode""": r"""batch""",
        r"""output_format""": r"""mp3_24000_160""",
        r"""voice_settings""": {
            r"""speed""": 1,
        },
    }

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode(r"""utf-8"""),
        headers={
            r"""xi-api-key""": api_key,
            r"""content-type""": r"""application/json""",
            r"""idempotency-key""": str(uuid.uuid4()),
        },
        method=r"""POST""",
    )

    try:
        with urllib.request.urlopen(request) as response:
            audio = response.read()
    except urllib.error.HTTPError as error:
        body = error.read().decode(
            r"""utf-8""",
            errors=r"""replace""",
        )

        raise RuntimeError(
            r"""Giggy returned HTTP {}: {}""".format(
                error.code,
                body,
            )
        ) from error

    OUTPUT_PATH.write_bytes(audio)

    print(
        r"""Wrote {} bytes to {}""".format(
            len(audio),
            OUTPUT_PATH,
        )
    )


if __name__ == r"""__main__""":
    main()
