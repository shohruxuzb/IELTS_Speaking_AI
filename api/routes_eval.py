import json
import tempfile
from typing import List

from fastapi import APIRouter, File, Form, UploadFile, Depends

from core.rate_limiter import check_rate_limit
from services.ai_evaluator import evaluate_ielts_with_improvements
from services.speech_service import transcribe_audio

router = APIRouter()


@router.post("/evaluate")
async def evaluate(
    questions: str = Form(...),
    answers: str = Form(...),
    audios: List[UploadFile] = File(None),
    username: str = Depends(check_rate_limit),
):
    """
    Evaluate IELTS speaking performance.
    - Supports Part 1 & 3 (3 Q/As) and Part 2 (1 Q/A).
    - Returns scores + improved versions of answers.
    - Requires authentication (Bearer token).
    """
    questions = json.loads(questions) if isinstance(questions, str) else questions
    answers = json.loads(answers) if isinstance(answers, str) else answers

    if audios:
        transcripts = []
        for audio in audios:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(await audio.read())
                transcripts.append(transcribe_audio(tmp.name))
        answers = transcripts

    if not questions or not answers or len(questions) != len(answers):
        return {"error": "Questions and answers must be same length and non-empty"}

    evaluation = evaluate_ielts_with_improvements(questions, answers)
    return {"answers": answers, "evaluation": evaluation}
