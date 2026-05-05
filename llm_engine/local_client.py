import requests
import time
from llm_engine.base import BaseLLMClient

class LocalClient(BaseLLMClient):

    def is_available(self) -> bool:
        return True

    def generate(self, prompt: str) -> str:

        OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

        for attempt in range(3):
            try:
                print("Calling Ollama locally...")
                response = requests.post(
                OLLAMA_URL,
                json={
                    "model": "llama3.1:latest",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.2
                    }
                },
                timeout=120
            )

                if response.status_code != 200:
                    print("Status Code:", response.status_code)
                    print("Response Text:", response.text)
                    time.sleep(1)
                    continue

                if not response.text.strip():
                    print("Empty response from Ollama")
                    time.sleep(1)
                    continue

                data = response.json()

                print("Ollama responded successfully.")
                return data.get("response", "")

            except Exception as e:
                print(f"Retry {attempt+1} failed:", e)
                time.sleep(1)

        print("Ollama not responding after retries.")
        return "AI service temporarily unavailable."