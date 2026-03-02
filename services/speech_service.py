def transcribe_audio(audio_path: str) -> str:
    """Transcribe speech using Whisper on Groq"""
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-large-v3",
            file=f
        )
    return transcript.text if transcript else ""

def synthesize_speech(text: str) -> bytes:
    """
    Convert text into speech (mp3) using Groq TTS.
    """
    try:
        response = client.audio.speech.create(
            model="whisper-tts",   # or "whisper-tts" depending on Groq support
            voice="alloy",            # choose available voice
            input=text,
        )
        return response.audio  # raw audio bytes
    except Exception as e:
        print("TTS error:", e)
        return b""
