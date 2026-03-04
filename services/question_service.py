import re
import random

from groq import Groq
from core.config import GROQ_API_KEY
from core.logging import get_logger
from utils.text_utils import normalize_question

client = Groq(api_key=GROQ_API_KEY)
logger = get_logger(__name__)

# In-memory set to track already-asked questions within a session
asked_questions: set = set()


FALLBACK_QUESTIONS = {
    "part1": [
        "What is your full name?",
        "Where are you from?",
        "Do you work or are you a student?",
        "What do you like about your hometown?",
        "Do you prefer to study in the morning or in the evening?",
        "What hobbies did you have when you were a child?",
        "How often do you listen to music?",
        "Do you prefer to travel alone or with others?",
        "What is your favorite type of food?",
        "How do you usually spend your weekends?"
    ],
    "part2": [
        "Describe a beautiful place you have visited.\n- Where it is\n- When you went there\n- What you did there\n- And explain why you think it's beautiful.",
        "Talk about a book you recently read.\n- What the book is\n- What it is about\n- Why you decided to read it\n- And explain if you liked it or not.",
        "Describe a person who has influenced you.\n- Who they are\n- How you know them\n- What they are like\n- And explain why they influenced you.",
        "Talk about a gift you received that was special to you.\n- What the gift was\n- Who gave it to you\n- Why they gave it to you\n- And explain why it was special."
    ],
    "part3": [
        "How has technology changed the way people communicate in your country?",
        "Do you think it is important for children to learn about art and music?",
        "In your opinion, what are the most important qualities of a good leader?",
        "How do you think tourism affects the environment and local culture?",
        "Should governments do more to protect the environment?",
        "Is it better for people to live in a city or in the countryside?"
    ]
}


def _generate_unique_question(prompt: str, part_type: str = "part1") -> dict:
    """Generic helper that ensures uniqueness of generated questions."""
    # If API key is placeholder, use fallback immediately
    if not GROQ_API_KEY or "placeholder" in GROQ_API_KEY.lower():
        logger.warning("GROQ_API_KEY is placeholder, using fallback for %s", part_type)
        return {"question": random.choice(FALLBACK_QUESTIONS.get(part_type, FALLBACK_QUESTIONS["part1"]))}

    try:
        question = ""
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
        logger.error("Question generation failed: %s. Using fallback.", e, exc_info=True)
        return {"question": random.choice(FALLBACK_QUESTIONS.get(part_type, FALLBACK_QUESTIONS["part1"]))}


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
    questions = []
    for _ in range(3):
        result = _generate_unique_question(prompt, part_type="part1")
        if "error" in result:
            return result
        questions.append(result["question"])
    return {"questions": questions}


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
    return _generate_unique_question(prompt, part_type="part2")


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
    questions = []
    for _ in range(3):
        result = _generate_unique_question(prompt, part_type="part3")
        if "error" in result:
            return result
        questions.append(result["question"])
    return {"questions": questions}
