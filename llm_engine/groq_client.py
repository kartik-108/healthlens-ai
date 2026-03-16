import os
from llm_engine.base import BaseLLMClient

try:
    from groq import Groq
except ImportError:
    Groq = None


class GroqClient(BaseLLMClient):
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.enabled = os.getenv("ENABLE_GROQ", "false").lower() == "true"
        self.client = Groq(api_key=self.api_key) if self.api_key and Groq else None

    def is_available(self) -> bool:
        return bool(self.client and self.enabled)

    def generate(self, prompt: str) -> dict:
        chat = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
        )

        text = chat.choices[0].message.content

        return {
            "analysis": text[:300],
            "possible_conditions": [],
            "risk_level": "moderate",
            "medicine_info": [],
            "advice": "Consult a doctor if symptoms persist."
        }
