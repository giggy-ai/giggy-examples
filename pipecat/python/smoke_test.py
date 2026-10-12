import asyncio

import aiohttp

from giggy_tts import GiggyTTSService


async def async_main() -> None:
    async with aiohttp.ClientSession() as session:
        service = GiggyTTSService(
            api_key=r"""giggy_smoke_test_not_a_real_key""",
            voice_id=r"""00000000-0000-0000-0000-000000000000""",
            aiohttp_session=session,
            sample_rate=24000,
            speed=1.0,
        )

        if service is None:
            raise RuntimeError(
                r"""GiggyTTSService construction failed."""
            )

        for unsupported_rate in (8000, 16000, 22050):
            try:
                GiggyTTSService(api_key="fake-key", voice_id="fake-voice", aiohttp_session=session,
                                sample_rate=unsupported_rate)
            except ValueError:
                pass
            else:
                raise AssertionError("Unsupported Streaming sample rate accepted")

        print(
            r"""Pipecat GiggyTTSService constructed successfully."""
        )


def main() -> None:
    asyncio.run(
        async_main()
    )


if __name__ == r"""__main__""":
    main()
