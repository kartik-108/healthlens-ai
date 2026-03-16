# llm_engine/base.py

class BaseLLMClient:
    def generate(self, prompt: str) -> dict:
        raise NotImplementedError("LLM clients must implement generate()")
