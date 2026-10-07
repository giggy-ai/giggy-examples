import os

from livekit.plugins import openai


GIGGY_BASE_URL = r"""https://giggy.ai/v1"""


def create_giggy_tts() -> openai.TTS:
    api_key = os.environ.get(r"""GIGGY_API_KEY""")
    voice_id = os.environ.get(r"""GIGGY_VOICE_ID""")

    if not api_key:
        raise RuntimeError(
            r"""Set GIGGY_API_KEY before creating the LiveKit TTS client."""
        )

    if not voice_id:
        raise RuntimeError(
            r"""Set GIGGY_VOICE_ID before creating the LiveKit TTS client."""
        )

    return openai.TTS(
        model=r"""giggyspeech""",
        voice=voice_id,
        api_key=api_key,
        base_url=GIGGY_BASE_URL,
        response_format=r"""pcm""",
    )
