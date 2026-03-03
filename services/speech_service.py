from groq import Groq
from core.config import GROQ_API_KEY
from core.logging import get_logger

client = Groq(api_key=GROQ_API_KEY)
logger = get_logger(__name__)


def transcribe_audio(audio_path: str) -> str:
    """Transcribe speech using Whisper on Groq."""
    try:
        with open(audio_path, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=f
            )
        return transcript.text if transcript else ""
    except Exception as e:
        logger.error("Audio transcription failed for '%s': %s", audio_path, e, exc_info=True)
        return ""


def synthesize_speech(text: str) -> bytes:
    """
    Convert text into speech (mp3) using Groq TTS.
    Returns raw audio bytes, or empty bytes on failure.
    """
    try:
        response = client.audio.speech.create(
            model="playai-tts",
            voice="Fritz-PlayAI",
            input=text,
            response_format="mp3",
        )
        return response.read()
    except Exception as e:
        logger.error("TTS synthesis failed: %s", e, exc_info=True)
        return b""
