from pydantic import BaseModel
from typing import List, Optional


class EvaluationResult(BaseModel):
    """Shape of the AI evaluation output for one part."""
    overall_band: float
    fluency: float
    vocabulary: float
    grammar: float
    pronunciation: float
    strengths: List[str]
    weaknesses: List[str]
    improved_answers: List[str]


class AggregateResult(BaseModel):
    """Shape of the final aggregated IELTS result across all three parts."""
    overall_band: float
    fluency: float
    vocabulary: float
    grammar: float
    pronunciation: float
    strengths: List[str]
    weaknesses: List[str]


class QuestionResponse(BaseModel):
    """Single question response."""
    question: str
    note: Optional[str] = None


class QuestionsResponse(BaseModel):
    """Multiple questions response."""
    questions: List[str]
