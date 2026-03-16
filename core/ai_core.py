import os
import json
import re
from llm_engine.local_client import LocalClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYSTEM_PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "system_prompt.txt")


def load_system_prompt() -> str:
    if not os.path.exists(SYSTEM_PROMPT_PATH):
        raise FileNotFoundError(f"System prompt not found at {SYSTEM_PROMPT_PATH}")

    with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(user_message: str) -> str:
    system_prompt = load_system_prompt()

    structured_instruction = """
Return ONLY valid JSON in this format:

{
  "analysis": "",
  "possible_conditions": [],
  "risk_level": "",
  "medicine_info": [],
  "advice": ""
}

Do NOT add explanation.
Do NOT use markdown.
Return raw JSON only.
"""

    return f"{system_prompt}\n\nUSER MESSAGE:\n{user_message}\n\n{structured_instruction}"


def extract_json(text: str) -> dict:
    try:
        text = re.sub(r"```json|```", "", text).strip()
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("No JSON found")
    except:
        return {
            "analysis": "Unable to analyze symptoms at the moment.",
            "possible_conditions": [],
            "risk_level": "low",
            "medicine_info": [],
            "advice": "Please consult a doctor if symptoms persist."
        }


def run_ai_pipeline(user_message: str):
    client = LocalClient()
    prompt = build_prompt(user_message)

    raw_output = client.generate(prompt)

    print("\n===== OLLAMA RAW OUTPUT =====\n")
    print(raw_output)
    print("\n=============================\n")

    return extract_json(raw_output)