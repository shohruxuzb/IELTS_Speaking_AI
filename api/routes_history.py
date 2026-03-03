from fastapi import APIRouter, Depends, HTTPException, status

from core.auth import get_current_user
from core.logging import get_logger
from services.user_service import get_user_id
from services.history_service import get_user_history, get_session_detail, get_progress

router = APIRouter(prefix="/history", tags=["History"])
logger = get_logger(__name__)


@router.get("")
async def list_history(limit: int = 20, username: str = Depends(get_current_user)):
    """Return the last N evaluation sessions for the current user."""
    user_id = get_user_id(username)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return get_user_history(user_id, limit=limit)


@router.get("/progress")
async def progress(username: str = Depends(get_current_user)):
    """Return band scores over time — for dashboard charts."""
    user_id = get_user_id(username)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return get_progress(user_id)


@router.get("/{session_id}")
async def session_detail(session_id: str, username: str = Depends(get_current_user)):
    """Return full Q/A pairs, transcripts, improvements and scores for one session."""
    detail = get_session_detail(session_id)
    if not detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")
    return detail
