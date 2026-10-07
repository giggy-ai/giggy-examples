import asyncio
import os

from giggy_tts import create_giggy_tts


async def main() -> None:
    if os.environ.get("GIGGY_ALLOW_BILLABLE_SMOKE") != "1":
        raise RuntimeError("Set GIGGY_ALLOW_BILLABLE_SMOKE=1 to authorize synthesis.")
    if not os.environ.get("GIGGY_API_KEY") or not os.environ.get("GIGGY_VOICE_ID"):
        raise RuntimeError("Set GIGGY_API_KEY and GIGGY_VOICE_ID.")

    tts = create_giggy_tts()
    total_bytes = 0
    try:
        stream = tts.synthesize("Hello from Giggy LiveKit.")
        async for event in stream:
            total_bytes += len(event.frame.data)
    finally:
        await tts.aclose()
    if total_bytes <= 0:
        raise RuntimeError("LiveKit returned no speech audio.")
    print(f"LiveKit synthesis succeeded: {total_bytes} bytes")


if __name__ == "__main__":
    asyncio.run(main())
