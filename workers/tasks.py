import os
import json

from workers.celery_app import celery_app
from core.cache import cache_get, cache_set, make_hash_key
from core.config import CACHE_TTL_EVALUATIONS, JOB_TTL
from core.logging import get_logger
from services.speech_service import transcribe_audio
from services.ai_evaluator import evaluate_ielts_with_improvements
from services.history_service import save_session
from services.user_service import get_user_id

logger = get_logger(__name__)


# ── Job store helpers ─────────────────────────────────────────────────────────

def _job_key(job_id: str) -> str:
    return f"job:{job_id}"


def set_job_result(job_id: str, result: dict) -> None:
    cache_set(_job_key(job_id), result, JOB_TTL)


def get_job_result(job_id: str) -> dict | None:
    return cache_get(_job_key(job_id))


# ── Celery task ───────────────────────────────────────────────────────────────

@celery_app.task(bind=True, name="workers.tasks.run_evaluation")
def run_evaluation(
    self,
    job_id: str,
    questions: list,
    answers: list,
    audio_paths: list,
    username: str = "",
    part: int = 1,
):
    """
    Background task:
    1. Transcribe audio via Whisper (if provided).
    2. Check evaluation cache — skip LLM on hit.
    3. Run LLM evaluation.
    4. Cache evaluation result.
    5. Persist session to Supabase.
    6. Store job result in Redis for client polling.
    """
    try:
        # ── Step 1: Transcribe ────────────────────────────────────────────────
        if audio_paths:
            transcripts = []
            for path in audio_paths:
                transcript = transcribe_audio(path)
                transcripts.append(transcript)
                try:
                    os.remove(path)
                except OSError:
                    pass
            answers = transcripts

        # ── Step 2: Check evaluation cache ───────────────────────────────────
        eval_cache_key = f"ielts:eval:{make_hash_key(questions, answers)}"
        cached_eval = cache_get(eval_cache_key)

        if cached_eval is not None:
            logger.info("Evaluation cache HIT for job %s", job_id)
            evaluation = cached_eval
        else:
            # ── Step 3: Run LLM ───────────────────────────────────────────────
            logger.info("Evaluation cache MISS for job %s — calling LLM", job_id)
            evaluation = evaluate_ielts_with_improvements(questions, answers)

            if "error" in evaluation:
                set_job_result(job_id, {"status": "error", "detail": evaluation["error"]})
                return

            # ── Step 4: Cache result ──────────────────────────────────────────
            cache_set(eval_cache_key, evaluation, CACHE_TTL_EVALUATIONS)

        # ── Step 5: Persist to Supabase ───────────────────────────────────────
        if username:
            user_id = get_user_id(username)
            if user_id:
                improved = evaluation.get("improved_answers", [""] * len(answers))
                save_session(
                    user_id=user_id,
                    part=part,
                    questions=questions,
                    answers=answers,
                    improved_answers=improved,
                    scores=evaluation,
                )
            else:
                logger.warning("Could not find user_id for username '%s' — skipping DB save", username)

        # ── Step 6: Return result to client ───────────────────────────────────
        result = {"answers": answers, "evaluation": evaluation}
        set_job_result(job_id, {"status": "done", "result": result, "cached": cached_eval is not None})

    except Exception as exc:
        logger.error("run_evaluation task failed for job %s: %s", job_id, exc, exc_info=True)
        set_job_result(job_id, {"status": "error", "detail": "Evaluation failed. Please try again."})
