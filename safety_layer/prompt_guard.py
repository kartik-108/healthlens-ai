import re

# keywords that indicate prescription intent
BLOCK_KEYWORDS = [
    "which medicine",
    "what medicine",
    "suggest medicine",
    "prescribe",
    "dose",
    "dosage",
    "mg",
    "milligram",
    "how many times",
    "kitni baar",
    "kitna dose",
    "tablet loon",
    "medicine loon",
    "dawai loon"
]

SAFE_REWRITE_MESSAGE = (
    "I can help by analyzing symptoms and giving general health information. "
    "I cannot prescribe medicines or suggest dosage."
)

def guard_user_input(user_message: str) -> str:
    """
    Checks if user is asking for prescription-related help.
    If yes, rewrites message to a safe form.
    """
    msg_lower = user_message.lower()

    for keyword in BLOCK_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", msg_lower):
            return SAFE_REWRITE_MESSAGE + " Symptoms provided: " + user_message

    return user_message