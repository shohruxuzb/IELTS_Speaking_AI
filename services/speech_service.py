from groq import Groq
from core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def transcribe_audio(audio_path: str) -> str:
    """Transcribe speech using Whisper on Groq."""
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=f
        )
    return transcript.text if transcript else ""


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
        print("TTS error:", e)
        return b""
