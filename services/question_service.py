def normalize_question(q: str) -> str:
    """Normalize a question to detect duplicates by meaning (basic)."""
    q = q.lower().strip()
    q = re.sub(
        r'^(can you|could you|do you think|describe|talk about|tell me about|would you rather|if you could)\s+',
        '',
        q,
    )
    q = re.sub(r'[?.!,]', '', q)  # remove punctuation
    return q.strip()


def _generate_unique_question(prompt: str) -> dict:
    """Generic helper that ensures uniqueness of generated questions."""
    try:
        for _ in range(5):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=1.0,
                top_p=1,
                presence_penalty=1.2,
                frequency_penalty=0.9,
                max_tokens=150,
            )

            question = response.choices[0].message.content.strip()
            normalized = normalize_question(question)

            if normalized not in asked_questions:
                asked_questions.add(normalized)

                # reset after 200 unique questions
                if len(asked_questions) > 200:
                    asked_questions.clear()
                    asked_questions.add(normalized)

                return {"question": question}

        return {"question": question, "note": "⚠️ Might be semantically similar"}
    except Exception as e:
        return {"error": str(e)}


# ----------- IELTS PART-SPECIFIC GENERATORS -----------

def generate_part1_questions() -> dict:
    """Generate 3 IELTS Part 1 questions (short, everyday)."""
    prompt = """
    Generate ONE IELTS Speaking Part 1 question.

    Requirements:
    - Short, direct, and about familiar everyday topics 
      (hometown, hobbies, food, studies, work, friends, family, daily routine, etc.)
    - Not too abstract.
    - Suitable for a 20–30 second answer.
    - Return ONLY the question text.
    """
    return {"questions": [_generate_unique_question(prompt)["question"] for _ in range(3)]}


def generate_part2_question() -> dict:
    """Generate 1 IELTS Part 2 cue card question."""
    prompt = """
    Generate ONE IELTS Speaking Part 2 "Cue Card" style question.

    Requirements:
    - Start with "Describe ..." or "Talk about ..."
    - Include 3–4 bullet points (using dashes) that guide the candidate.
    - Topic should be about people, experiences, places, or objects.
    - Suitable for a 1–2 minute long answer.
    - Return ONLY the question text with bullet points.
    """
    return _generate_unique_question(prompt)


def generate_part3_questions() -> dict:
    """Generate 3 IELTS Part 3 abstract, discussion questions."""
    prompt = """
    Generate ONE IELTS Speaking Part 3 discussion question.

    Requirements:
    - Abstract, opinion-based, and analytical.
    - Related to society, culture, education, technology, future, or global issues.
    - Suitable for a 30–40 second thoughtful answer.
    - Return ONLY the question text.
    """
    return {"questions": [_generate_unique_question(prompt)["question"] for _ in range(3)]}


# ----------- API ROUTES -----------

@app.get("/generate-part1")
async def generate_part1():
    return generate_part1_questions()

@app.get("/generate-part2")
async def generate_part2():
    return generate_part2_question()

@app.get("/generate-part3")
async def generate_part3():
    return generate_part3_questions()

