import asyncio
import os

import aiohttp
from giggy_tts import GiggyTTSService
from pipecat.frames.frames import ErrorFrame, TTSAudioRawFrame, TTSSpeakFrame
from pipecat.pipeline.worker import PipelineParams
from pipecat.tests.utils import run_test


async def main() -> None:
    if os.environ.get("GIGGY_ALLOW_BILLABLE_SMOKE") != "1":
        raise RuntimeError("Set GIGGY_ALLOW_BILLABLE_SMOKE=1 to authorize synthesis.")
    api_key = os.environ["GIGGY_API_KEY"]
    voice_id = os.environ["GIGGY_VOICE_ID"]
    total_bytes = 0
    async with aiohttp.ClientSession() as session:
        tts = GiggyTTSService(api_key=api_key, voice_id=voice_id, aiohttp_session=session)
        down_frames, up_frames = await run_test(
            tts,
            frames_to_send=[TTSSpeakFrame("Hello from Giggy Pipecat.")],
            pipeline_params=PipelineParams(audio_out_sample_rate=24000),
            enable_rtvi=False,
        )
        errors = [frame.error for frame in up_frames if isinstance(frame, ErrorFrame)]
        if errors:
            raise RuntimeError(str(errors[0]))
        for frame in down_frames:
            if isinstance(frame, TTSAudioRawFrame):
                total_bytes += len(frame.audio)
    if total_bytes <= 0:
        raise RuntimeError("Pipecat returned no speech audio.")
    print(f"Pipecat synthesis succeeded: {total_bytes} bytes")


if __name__ == "__main__":
    asyncio.run(main())
