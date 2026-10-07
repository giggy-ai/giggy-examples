import asyncio
import os
import uuid

import aiohttp
from pipecat.frames.frames import ErrorFrame, TTSAudioRawFrame
from giggy_tts import GiggyTTSService


async def main() -> None:
    if os.environ.get("GIGGY_ALLOW_BILLABLE_SMOKE") != "1":
        raise RuntimeError("Set GIGGY_ALLOW_BILLABLE_SMOKE=1 to authorize synthesis.")
    api_key = os.environ["GIGGY_API_KEY"]
    voice_id = os.environ["GIGGY_VOICE_ID"]
    total_bytes = 0
    async with aiohttp.ClientSession() as session:
        tts = GiggyTTSService(api_key=api_key, voice_id=voice_id, aiohttp_session=session)
        async for frame in tts.run_tts("Hello from Giggy Pipecat.", str(uuid.uuid4())):
            if isinstance(frame, ErrorFrame):
                raise RuntimeError(str(frame.error))
            if isinstance(frame, TTSAudioRawFrame):
                total_bytes += len(frame.audio)
    if total_bytes <= 0:
        raise RuntimeError("Pipecat returned no speech audio.")
    print(f"Pipecat synthesis succeeded: {total_bytes} bytes")


if __name__ == "__main__":
    asyncio.run(main())
