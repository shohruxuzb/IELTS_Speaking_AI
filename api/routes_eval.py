
@app.post("/evaluate")
async def evaluate(
    questions: str = Form(...),   # JSON string of questions
    answers: str = Form(...),     # JSON string of answers (manual text or transcripts)
    audios: List[UploadFile] = File(None)  # Optional audio list
):
    """
    Evaluate IELTS speaking performance.
    - Supports Part 1 & 3 (3 Q/As) and Part 2 (1 Q/A).
    - Returns scores + improved versions of answers.
    """

    import json
    questions = json.loads(questions) if isinstance(questions, str) else questions
    answers = json.loads(answers) if isinstance(answers, str) else answers

    # If audio is uploaded, transcribe each and replace answers
    if audios:
        transcripts = []
        for audio in audios:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(await audio.read())
                transcripts.append(transcribe_audio(tmp.name))
        answers = transcripts

    # Safety check
    if not questions or not answers or len(questions) != len(answers):
        return {"error": "Questions and answers must be same length and non-empty"}

    evaluation = evaluate_ielts_with_improvements(questions, answers)
    return {"answers": answers, "evaluation": evaluation}
