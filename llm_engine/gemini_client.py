import os
from llm_engine.base import BaseLLMClient

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class GeminiClient(BaseLLMClient):
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.enabled = os.getenv("ENABLE_GEMINI", "false").lower() == "true"

        if self.api_key and genai:
            genai.configure(api_key=self.api_key)

    def is_available(self) -> bool:
        return bool(self.api_key and self.enabled and genai)

    def generate(self, prompt: str) -> dict:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        text = response.text or ""

        # IMPORTANT: enforce JSON expectation via system prompt
        # Fallback parse-safe response
        return {
            "analysis": text[:300],
            "possible_conditions": [],
            "risk_level": "moderate",
            "medicine_info": [],
            "advice": "If symptoms persist or worsen, consult a doctor."
        }
def is_available(self) -> bool:
    print(
        "GEMINI CHECK →",
        "api_key:", bool(self.api_key),
        "enabled:", self.enabled,
        "lib:", bool(genai)
    )
    return bool(self.api_key and self.enabled and genai)
def generate(self, prompt: str) -> dict:
    print("🔥 USING GEMINI")