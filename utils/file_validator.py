import wave
import contextlib
from fastapi import HTTPException, UploadFile, status

from core.config import (
    ALLOWED_AUDIO_MIME_TYPES,
    MAX_AUDIO_DURATION_SEC,
    MAX_FILE_SIZE_MB,
)
from core.logging import get_logger

logger = get_logger(__name__)

MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


async def validate_audio_file(file: UploadFile) -> bytes:
    """
    Read and validate an uploaded audio file.

    Checks:
    1. MIME type must be in ALLOWED_AUDIO_MIME_TYPES
    2. File size must not exceed MAX_FILE_SIZE_MB
    3. Audio duration must not exceed MAX_AUDIO_DURATION_SEC

    Returns the raw bytes so the caller doesn't have to re-read the file.
    Raises HTTPException 400 on any violation.
    """

    # ── 1. MIME type check ───────────────────────────────────────────────────
    content_type = (file.content_type or "").lower()
    if content_type not in ALLOWED_AUDIO_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported file type: '{content_type}'. "
                f"Allowed types: {', '.join(sorted(ALLOWED_AUDIO_MIME_TYPES))}."
            ),
        )

    # ── 2. Size check ────────────────────────────────────────────────────────
    data = await file.read()
    if len(data) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Maximum allowed size is {MAX_FILE_SIZE_MB} MB.",
        )

    # ── 3. Duration check ────────────────────────────────────────────────────
    duration = _get_wav_duration(data) if content_type in ("audio/wav", "audio/x-wav") else _get_duration_mutagen(data, file.filename)

    if duration is not None and duration > MAX_AUDIO_DURATION_SEC:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Audio too long ({duration:.1f}s). "
                f"Maximum allowed duration is {MAX_AUDIO_DURATION_SEC}s."
            ),
        )

    return data


# ── Duration helpers ─────────────────────────────────────────────────────────

def _get_wav_duration(data: bytes) -> float | None:
    """Parse WAV header with stdlib — no external deps."""
    import io
    try:
        with contextlib.closing(wave.open(io.BytesIO(data))) as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / float(rate) if rate > 0 else None
    except Exception as exc:
        logger.warning("Could not read WAV duration: %s", exc)
        return None


def _get_duration_mutagen(data: bytes, filename: str | None) -> float | None:
    """Use mutagen for MP3 / OGG / M4A / WebM duration."""
    try:
        import io
        from mutagen import File as MutagenFile
        audio = MutagenFile(io.BytesIO(data), filename=filename)
        if audio and audio.info:
            return audio.info.length
    except ImportError:
        logger.warning("mutagen not installed — skipping duration check for non-WAV files.")
    except Exception as exc:
        logger.warning("Could not read audio duration via mutagen: %s", exc)
    return None
