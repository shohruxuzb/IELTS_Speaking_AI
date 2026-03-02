
@app.post("/mock-test-voice")
async def mock_test_voice(part1: list[str], part2: str, part3: list[str]):
    """
    Generate a full mock IELTS test audio:
    - Greeting
    - Part 1 questions
    - Part 2 cue card
    - Part 3 questions
    - Goodbye
    """

    script = []

    # Greeting
    script.append("Hello, welcome to your IELTS speaking mock test. Let's begin.")

    # Part 1
    script.append("Part one. I will ask you some questions about yourself and everyday topics.")
    for q in part1:
        script.append(q)

    # Part 2
    script.append("Now let's move on to part two. You will have a cue card.")
    script.append(part2)

    # Part 3
    script.append("Now we continue with part three. I will ask you some more discussion questions.")
    for q in part3:
        script.append(q)

    # Goodbye
    script.append("That concludes the IELTS speaking mock test. Thank you, and goodbye.")

    # Concatenate into one long script
    full_text = " ".join(script)

    # Convert to speech
    audio_bytes = synthesize_speech(full_text)

    if not audio_bytes:
        return {"error": "TTS generation failed"}

    return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/mpeg")
