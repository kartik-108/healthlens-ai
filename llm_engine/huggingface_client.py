from llm_engine.base import BaseLLMClient


class HuggingFaceClient(BaseLLMClient):
    def is_available(self) -> bool:
        # Disabled for now (free tier / cost control)
        return False

    def generate(self, prompt: str) -> dict:
        raise RuntimeError("HuggingFace LLM is disabled")
