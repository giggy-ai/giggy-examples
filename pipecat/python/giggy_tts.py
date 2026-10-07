from collections.abc import AsyncGenerator
from dataclasses import dataclass, field

import aiohttp

from pipecat.frames.frames import (
    ErrorFrame,
    Frame,
    TTSAudioRawFrame,
)
from pipecat.services.settings import TTSSettings
from pipecat.services.tts_service import TTSService
from pipecat.utils.tracing.service_decorators import traced_tts
from pipecat.utils.types import NOT_GIVEN, NotGiven


GIGGY_SPEECH_URL = r"""https://giggy.ai/v1/audio/speech"""


@dataclass
class GiggyTTSSettings(TTSSettings):
    speed: float | None | NotGiven = field(
        default_factory=lambda: NOT_GIVEN
    )


class GiggyTTSService(TTSService):
    Settings = GiggyTTSSettings
    _settings: GiggyTTSSettings

    def __init__(
        self,
        *,
        api_key: str,
        voice_id: str,
        aiohttp_session: aiohttp.ClientSession,
        sample_rate: int = 24000,
        speed: float = 1.0,
        **kwargs,
    ):
        if not api_key:
            raise ValueError(
                r"""api_key is required."""
            )

        if not voice_id:
            raise ValueError(
                r"""voice_id is required."""
            )

        if sample_rate not in {
            8000,
            16000,
            22050,
            24000,
        }:
            raise ValueError(
                r"""sample_rate must be 8000, 16000, 22050, or 24000."""
            )

        if speed < 0.25 or speed > 4:
            raise ValueError(
                r"""speed must be between 0.25 and 4."""
            )

        settings = self.Settings(
            model=r"""giggyspeech""",
            voice=voice_id,
            language=None,
            speed=speed,
        )

        super().__init__(
            sample_rate=sample_rate,
            push_start_frame=True,
            push_stop_frames=True,
            settings=settings,
            **kwargs,
        )

        self._api_key = api_key
        self._session = aiohttp_session

    def can_generate_metrics(self) -> bool:
        return True

    @traced_tts
    async def run_tts(
        self,
        text: str,
        context_id: str,
    ) -> AsyncGenerator[Frame | None, None]:
        voice_id = self._settings.voice
        speed = self._settings.speed

        if not voice_id:
            yield ErrorFrame(
                error=r"""Giggy voice ID is not configured."""
            )
            return

        payload = {
            r"""model""": r"""giggyspeech""",
            r"""input""": text,
            r"""voice""": voice_id,
            r"""response_format""": r"""pcm""",
            r"""sample_rate""": self.sample_rate,
            r"""speed""": speed if speed is not None else 1.0,
        }

        headers = {
            r"""Authorization""": (
                r"""Bearer """ + self._api_key
            ),
            r"""Content-Type""": r"""application/json""",
        }

        try:
            async with self._session.post(
                GIGGY_SPEECH_URL,
                json=payload,
                headers=headers,
            ) as response:
                if response.status != 200:
                    body = await response.text()

                    yield ErrorFrame(
                        error=(
                            r"""Giggy TTS returned HTTP {}: {}"""
                        ).format(
                            response.status,
                            body,
                        )
                    )
                    return

                content_type = response.headers.get(
                    r"""content-type""",
                    r"""""",
                )

                if (
                    content_type
                    and not content_type.startswith(
                        r"""application/octet-stream"""
                    )
                    and not content_type.startswith(
                        r"""audio/pcm"""
                    )
                ):
                    yield ErrorFrame(
                        error=(
                            r"""Giggy TTS returned an unexpected """
                            r"""Content-Type: {}"""
                        ).format(
                            content_type,
                        )
                    )
                    return

                await self.start_tts_usage_metrics(text)

                async for chunk in response.content.iter_chunked(
                    self.chunk_size
                ):
                    if not chunk:
                        continue

                    await self.stop_ttfb_metrics()

                    yield TTSAudioRawFrame(
                        chunk,
                        self.sample_rate,
                        1,
                        context_id=context_id,
                    )

        except aiohttp.ClientError as error:
            yield ErrorFrame(
                error=(
                    r"""Giggy TTS network error: {}"""
                ).format(
                    error,
                )
            )

        finally:
            await self.stop_ttfb_metrics()
