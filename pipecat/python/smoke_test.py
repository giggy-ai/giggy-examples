import asyncio

import aiohttp

from giggy_tts import GiggyTTSService


async def async_main() -> None:
    async with aiohttp.ClientSession() as session:
        service = GiggyTTSService(
            api_key=r"""giggy_sk_smoke_test_not_a_real_key""",
            voice_id=r"""00000000-0000-0000-0000-000000000000""",
            aiohttp_session=session,
            sample_rate=24000,
            speed=1.0,
        )

        if service is None:
            raise RuntimeError(
                r"""GiggyTTSService construction failed."""
            )

        print(
            r"""Pipecat GiggyTTSService constructed successfully."""
        )


def main() -> None:
    asyncio.run(
        async_main()
    )


if __name__ == r"""__main__""":
    main()
