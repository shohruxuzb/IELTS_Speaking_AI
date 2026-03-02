def evaluate_ielts_with_improvements(questions: List[str], answers: List[str]) -> dict:
    """
    Evaluate IELTS answers across one or multiple questions,
    and provide improved versions of each answer.
    """
    qa_pairs = "\n".join(
        [f"{i+1}. Q: \"{q}\" \n   A: \"{a}\"" for i, (q, a) in enumerate(zip(questions, answers))]
    )

    prompt = f"""
You are a certified IELTS examiner and English tutor. 
Evaluate the candidate's speaking performance strictly based on IELTS Band Descriptors.

Assessment Criteria:
- Fluency and Coherence
- Lexical Resource
- Grammatical Range and Accuracy
- Pronunciation

Tasks:
1. Give realistic sub-scores (0–9, steps of 0.5).
2. Give overall band score.
3. Mention strengths and weaknesses.
4. For each answer, provide an improved version (same meaning, but more natural and fluent).

Candidate’s responses:
{qa_pairs}

Return ONLY valid JSON with this structure:
{{
  "overall_band": float,
  "fluency": float,
  "vocabulary": float,
  "grammar": float,
  "pronunciation": float,
  "strengths": [list of strings],
  "weaknesses": [list of strings],
  "improved_answers": [list of improved answers, same length as input]
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=800,
        )
        text_output = response.choices[0].message.content
        result_json = json.loads(text_output[text_output.index("{"): text_output.rindex("}")+1])
        return result_json
    except Exception as e:
        return {"error": str(e)}

