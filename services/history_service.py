from typing import List, Optional
from core.database import get_db
from core.logging import get_logger

logger = get_logger(__name__)


def save_session(
    user_id: str,
    part: int,
    questions: List[str],
    answers: List[str],
    improved_answers: List[str],
    scores: dict,
) -> Optional[str]:
    """
    Persist a full evaluation session to Supabase.
    Returns the session UUID on success, or None on failure.
    """
    try:
        db = get_db()

        # 1. Create session row
        session_resp = db.table("sessions").insert({
            "user_id": user_id,
            "part": part,
        }).execute()

        if not session_resp.data:
            logger.error("Failed to create session row for user %s", user_id)
            return None

        session_id = session_resp.data[0]["id"]

        # 2. Insert Q/A entries
        entries = [
            {
                "session_id": session_id,
                "question": q,
                "transcript": a,
                "improved_answer": imp,
            }
            for q, a, imp in zip(questions, answers, improved_answers)
        ]
        db.table("speaking_entries").insert(entries).execute()

        # 3. Insert scores
        db.table("scores").insert({
            "session_id": session_id,
            "overall_band": scores.get("overall_band"),
            "fluency": scores.get("fluency"),
            "vocabulary": scores.get("vocabulary"),
            "grammar": scores.get("grammar"),
            "pronunciation": scores.get("pronunciation"),
            "strengths": scores.get("strengths", []),
            "weaknesses": scores.get("weaknesses", []),
        }).execute()

        logger.info("Session %s saved for user %s (part %d)", session_id, user_id, part)
        return session_id

    except Exception as e:
        logger.error("save_session failed for user %s: %s", user_id, e, exc_info=True)
        return None


def get_user_history(user_id: str, limit: int = 20) -> list:
    """Return the last `limit` sessions for a user, with band scores."""
    try:
        db = get_db()
        result = (
            db.table("sessions")
            .select("id, part, created_at, scores(overall_band, fluency, vocabulary, grammar, pronunciation)")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data or []
    except Exception as e:
        logger.error("get_user_history failed for user %s: %s", user_id, e, exc_info=True)
        return []


def get_session_detail(session_id: str) -> Optional[dict]:
    """Return full Q/A entries and scores for a single session."""
    try:
        db = get_db()
        session = (
            db.table("sessions")
            .select("id, part, created_at, speaking_entries(*), scores(*)")
            .eq("id", session_id)
            .single()
            .execute()
        )
        return session.data
    except Exception as e:
        logger.error("get_session_detail failed for session %s: %s", session_id, e, exc_info=True)
        return None


def get_progress(user_id: str) -> list:
    """
    Return overall band score over time for progress charts.
    One data point per session, ordered chronologically.
    """
    try:
        db = get_db()
        result = (
            db.table("sessions")
            .select("part, created_at, scores(overall_band, fluency, vocabulary, grammar, pronunciation)")
            .eq("user_id", user_id)
            .order("created_at", desc=False)
            .execute()
        )
        return result.data or []
    except Exception as e:
        logger.error("get_progress failed for user %s: %s", user_id, e, exc_info=True)
        return []
