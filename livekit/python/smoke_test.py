import os

from giggy_tts import create_giggy_tts


def main() -> None:
    os.environ.setdefault(
        r"""GIGGY_API_KEY""",
        r"""giggy_smoke_test_not_a_real_key""",
    )

    os.environ.setdefault(
        r"""GIGGY_VOICE_ID""",
        r"""00000000-0000-0000-0000-000000000000""",
    )

    tts = create_giggy_tts()

    if tts is None:
        raise RuntimeError(
            r"""create_giggy_tts returned None."""
        )

    print(
        r"""LiveKit Giggy TTS object constructed successfully."""
    )


if __name__ == r"""__main__""":
    main()
