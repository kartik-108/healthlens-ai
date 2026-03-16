import json
from llm_engine.gemini_client import GeminiClient
from llm_engine.groq_client import GroqClient
from llm_engine.huggingface_client import HuggingFaceClient
from llm_engine.local_client import LocalClient


class LLMRouter:
    def __init__(self):
        self.providers = [
            GeminiClient(),
            GroqClient(),
            HuggingFaceClient(),
            LocalClient()
        ]

    def generate(self, prompt: str) -> dict:
        for provider in self.providers:
            try:
                # Skip provider if not available
                if hasattr(provider, "is_available"):
                    if not provider.is_available():
                        continue

                print(f"➡️ Trying provider: {provider.__class__.__name__}")

                response = provider.generate(prompt)

                # Case 1: Already dict
                if isinstance(response, dict):
                    print(f"✅ Used provider: {provider.__class__.__name__}")
                    return response

                # Case 2: String → try JSON parsing
                if isinstance(response, str):
                    try:
                        parsed = json.loads(response)
                        print(f"✅ Used provider (parsed JSON string): {provider.__class__.__name__}")
                        return parsed
                    except json.JSONDecodeError:
                        print(f"⚠️ Invalid JSON from {provider.__class__.__name__}")
                        continue

            except Exception as e:
                print(f"❌ Provider failed: {provider.__class__.__name__} → {e}")
                continue

        # Absolute fallback (only if all providers fail)
        print("⚠️ All providers failed. Using fallback response.")

        return {
            "analysis": "Unable to analyze symptoms at the moment.",
            "possible_conditions": [],
            "risk_level": "low",
            "medicine_info": [],
            "advice": "Please consult a doctor if symptoms persist.",
            "disclaimer": "HealthLens AI is a health assistant, not a doctor."
        }