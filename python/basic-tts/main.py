import os
from pathlib import Path
from uuid import uuid4

import requests

API_URL = "https://giggy.ai/v1/text-to-speech"

payload = {
    "text": r"""Hello from Giggy's text-to-speech API.""",
    "voice_id": os.environ["GIGGY_VOICE_ID"],
    "model_id": "giggyspeech",
    "mode": "batch",
    "output_format": "mp3_24000_160",
    "voice_settings": {"speed": 1},
}

response = requests.post(
    API_URL,
    headers={
        "xi-api-key": os.environ["GIGGY_API_KEY"],
        "Content-Type": "application/json",
        "Idempotency-Key": str(uuid4()),
    },
    json=payload,
    timeout=600,
    allow_redirects=False,
)
response.raise_for_status()

if not response.headers.get("Content-Type", "").lower().startswith("audio/"):
    raise RuntimeError(
        f"Expected audio, received: {response.headers.get('Content-Type')}"
    )

Path("speech.mp3").write_bytes(response.content)
print("Saved speech.mp3")
