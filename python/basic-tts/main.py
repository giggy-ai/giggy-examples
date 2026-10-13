import os
from pathlib import Path
import argparse
import sys
import time

parser = argparse.ArgumentParser(description="Giggy TTS or recording-to-text walkthrough")
parser.add_argument("--stt", help="Local PCM16 mono 16-kHz WAV to transcribe")
parser.add_argument("--mode", choices=("batch", "fast", "streaming"), default="batch")
parser.add_argument("--output", help="Optional file for the final transcript")
args = parser.parse_args()
if args.stt:
    from giggy import Giggy
    client = Giggy(api_key=os.environ["GIGGY_API_KEY"])
    if args.mode == "streaming":
        generation_uuid = None
        with client.transcriptions.stream(args.stt) as events:
            for event, data in events:
                if event == "generation_created":
                    generation_uuid = data["generation"]["generation_uuid"]
                    print("Generation:", generation_uuid, file=sys.stderr)
                elif event == "transcript_chunk":
                    print("Preview:", data["text"], file=sys.stderr)
        if not generation_uuid:
            raise RuntimeError("No admission UUID received; inspect History before resubmitting")
    else:
        admission = client.transcriptions.submit(args.stt, mode=args.mode)
        generation_uuid = admission["generation"]["generation_uuid"]
        print("Generation:", generation_uuid, file=sys.stderr)
    deadline = time.monotonic() + 1800
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError(f"Inspect generation {generation_uuid}; do not upload again automatically")
        generation = client.transcriptions.get(generation_uuid, timeout=min(30, remaining))
        if generation["status"] == "completed":
            result = client.transcriptions.result(generation_uuid, timeout=remaining)
            break
        if generation["status"] in ("failed", "cancelled", "admission_failed"):
            raise RuntimeError(f"Generation {generation_uuid}: {generation['status']}")
        time.sleep(min(2.5, remaining))
    print(result["text"])
    if args.output:
        Path(args.output).write_text(result["text"], encoding="utf-8")
else:
    import requests
    API_URL = "https://giggy.ai/v1/text-to-speech"

    payload = {
        "text": r"""Welcome to Giggy's free text-to-speech API.""",
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
        },
        json=payload,
        timeout=600,
    )
    response.raise_for_status()

    if not response.headers.get("Content-Type", "").lower().startswith("audio/"):
        raise RuntimeError(
            f"Expected audio, received: {response.headers.get('Content-Type')}"
        )

    Path("speech.mp3").write_bytes(response.content)
    print("Saved speech.mp3")
