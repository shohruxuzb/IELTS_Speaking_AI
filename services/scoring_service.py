from typing import List, Dict

from groq import Groq
from core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def aggregate_evaluations(evaluations: List[Dict]) -> dict:
    """
    Combine multiple evaluations (from Part 1, 2, 3) into one overall IELTS result.
    Weighted scoring:
        Part 1 -> 25%
        Part 2 -> 40%
        Part 3 -> 35%
    """
    if not evaluations or len(evaluations) != 3:
        return {"error": "Expected exactly 3 evaluations (Part 1, Part 2, Part 3)"}

    weights = [0.25, 0.40, 0.35]  # Part 1, Part 2, Part 3
    criteria = ["fluency", "vocabulary", "grammar", "pronunciation", "overall_band"]

    weighted_scores = {c: 0.0 for c in criteria}
    strengths, weaknesses = [], []

    for i, ev in enumerate(evaluations):
        if "error" in ev:
            continue

        try:
            for c in criteria:
                weighted_scores[c] += float(ev[c]) * weights[i]

            strengths.extend(ev.get("strengths", []))
            weaknesses.extend(ev.get("weaknesses", []))
        except Exception:
            continue

    overall_result = {
        "overall_band": round(weighted_scores["overall_band"], 1),
        "fluency": round(weighted_scores["fluency"], 1),
        "vocabulary": round(weighted_scores["vocabulary"], 1),
        "grammar": round(weighted_scores["grammar"], 1),
        "pronunciation": round(weighted_scores["pronunciation"], 1),
        "strengths": list(set(strengths)),   # remove duplicates
        "weaknesses": list(set(weaknesses))  # remove duplicates
    }

    return overall_result
