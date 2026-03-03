import json
import tempfile
import uuid
from typing import List, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Depends, Query, status
from fastapi.responses import JSONResponse

from core.rate_limiter import check_rate_limit
from core.cache import cache_set
from core.config import JOB_TTL
from core.logging import get_logger
from utils.file_validator import validate_audio_file
from workers.tasks import run_evaluation

router = APIRouter()
logger = get_logger(__name__)


@router.post("/evaluate", status_code=status.HTTP_202_ACCEPTED)
async def evaluate(
    questions: str = Form(...),
    answers: str = Form(...),
    part: int = Form(1),                       # which IELTS part (1 | 2 | 3)
    audios: List[UploadFile] = File(None),
    username: str = Depends(check_rate_limit),
):
    """
    Submit an IELTS evaluation job.

    Returns `{"job_id": "..."}` immediately (HTTP 202).
    Poll `GET /jobs/{job_id}` for the result.
    Audio files: max 10 MB, max 180 s, WAV/MP3/OGG/M4A/WebM only.
    """
    # ── Parse JSON inputs ─────────────────────────────────────────────────────
    try:
        questions_parsed = json.loads(questions) if isinstance(questions, str) else questions
        answers_parsed = json.loads(answers) if isinstance(answers, str) else answers
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'questions' and 'answers' must be valid JSON arrays.",
        )

    if not questions_parsed or not answers_parsed or len(questions_parsed) != len(answers_parsed):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Questions and answers must be non-empty and the same length.",
        )

    if part not in (1, 2, 3):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'part' must be 1, 2, or 3.",
        )

    # ── Validate and save audio to named temp files ───────────────────────────
    audio_paths: List[str] = []
    if audios:
        for audio in audios:
            audio_bytes = await validate_audio_file(audio)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_bytes)
                audio_paths.append(tmp.name)

    # ── Enqueue background job ────────────────────────────────────────────────
    job_id = str(uuid.uuid4())
    cache_set(f"job:{job_id}", {"status": "pending"}, JOB_TTL)

    run_evaluation.delay(
        job_id,
        questions_parsed,
        answers_parsed,
        audio_paths,
        username=username,
        part=part,
    )

    logger.info("Evaluation job %s queued for user '%s' (part %d)", job_id, username, part)

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={"job_id": job_id, "status": "pending"},
    )
