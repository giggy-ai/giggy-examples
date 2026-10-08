import os
from pathlib import Path

import requests

PROMPTS = {
    "short": r"""Hello! Welcome to our text-to-speech comparison.""",
    "numbers": r"""Your order number is 12345.
The total is $29.99, and delivery is scheduled
for October 15, 2026.""",
    "narration": r"""The morning sun rose above the mountains.
A gentle breeze moved through the trees as the
town slowly came to life.""",
}

# Validate configuration before sending any potentially chargeable requests.
GIGGY_API_KEY = os.environ["GIGGY_API_KEY"]
GIGGY_VOICE_ID = os.environ["GIGGY_VOICE_ID"]
ELEVENLABS_API_KEY = os.environ["ELEVENLABS_API_KEY"]
ELEVENLABS_VOICE_ID = os.environ["ELEVENLABS_VOICE_ID"]

OUTPUT = Path("outputs")
OUTPUT.mkdir(exist_ok=True)


def generate(url, api_key, payload, destination, params=None):
    response = requests.post(
        url,
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        json=payload,
        params=params,
        timeout=600,
    )
    response.raise_for_status()
    if not response.headers.get("Content-Type", "").lower().startswith("audio/"):
        raise RuntimeError(
            f"Expected audio, received: {response.headers.get('Content-Type')}"
        )
    destination.write_bytes(response.content)


for name, text in PROMPTS.items():
    generate(
        "https://giggy.ai/v1/text-to-speech",
        GIGGY_API_KEY,
        {
            "text": text,
            "voice_id": GIGGY_VOICE_ID,
            "model_id": "giggyspeech",
            "mode": "fast",
            "output_format": "mp3_24000_160",
            "voice_settings": {"speed": 1},
        },
        OUTPUT / f"{name}-giggy.mp3",
    )
    generate(
        "https://api.elevenlabs.io/v1/text-to-speech/" + ELEVENLABS_VOICE_ID,
        ELEVENLABS_API_KEY,
        {"text": text, "model_id": "eleven_flash_v2_5"},
        OUTPUT / f"{name}-elevenlabs.mp3",
        params={"output_format": "mp3_44100_128"},
    )

print("Saved comparison audio to outputs/")
