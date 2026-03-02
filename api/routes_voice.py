import io
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from core.rate_limiter import check_rate_limit
from services.speech_service import synthesize_speech

router = APIRouter()


@router.post("/mock-test-voice")
async def mock_test_voice(
    part1: List[str],
    part2: str,
    part3: List[str],
    username: str = Depends(check_rate_limit),
):
    """
    Generate a full mock IELTS test audio.
    Requires authentication (Bearer token).
    """
    script = []

    script.append("Hello, welcome to your IELTS speaking mock test. Let's begin.")

    script.append("Part one. I will ask you some questions about yourself and everyday topics.")
    for q in part1:
        script.append(q)

    script.append("Now let's move on to part two. You will have a cue card.")
    script.append(part2)

    script.append("Now we continue with part three. I will ask you some more discussion questions.")
    for q in part3:
        script.append(q)

    script.append("That concludes the IELTS speaking mock test. Thank you, and goodbye.")

    full_text = " ".join(script)
    audio_bytes = synthesize_speech(full_text)

    if not audio_bytes:
        return {"error": "TTS generation failed"}

    return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/mpeg")
