import re


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
