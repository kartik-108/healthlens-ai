import re
from .disclaimer import DISCLAIMER_TEXT

# patterns that indicate dosage or prescription
UNSAFE_PATTERNS = [
    r"\b\d+\s*mg\b",
    r"\b\d+\s*milligram\b",
    r"\b\d+\s*times?\s*(a|per)?\s*day\b",
    r"\bonce\s*a\s*day\b",
    r"\btwice\s*a\s*day\b",
    r"\bthrice\s*a\s*day\b",
    r"\bevery\s*\d+\s*hours?\b",
]

def clean_text(text: str) -> str:
    """
    Removes unsafe dosage or prescription-related content from text.
    """
    cleaned = text
    for pattern in UNSAFE_PATTERNS:
        cleaned = re.sub(pattern, "[removed]", cleaned, flags=re.IGNORECASE)
    return cleaned


def filter_llm_response(response: dict) -> dict:
    """
    Cleans LLM response fields and appends disclaimer.
    """
    safe_response = {}

    for key, value in response.items():
        if isinstance(value, str):
            safe_response[key] = clean_text(value)
        elif isinstance(value, list):
            safe_response[key] = [clean_text(v) for v in value]
        else:
            safe_response[key] = value

    # Always enforce disclaimer
    safe_response["disclaimer"] = DISCLAIMER_TEXT

    return safe_response