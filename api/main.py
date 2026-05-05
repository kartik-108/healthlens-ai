from core.env_loader import load_dotenv  # noqa: F401
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.ai_core import run_ai_pipeline
from safety_layer.prompt_guard import guard_user_input

# 👋 Greeting detection
greetings = ["hi", "hello", "hey", "good morning", "good evening"]

def is_greeting(message: str) -> bool:
    message = message.lower().strip()
    return any(greet in message for greet in greetings)


# 🔒 Health keyword detection
health_keywords = [
    "pain","fever","headache","cough","cold","vomit",
    "nausea","infection","symptom","medicine","disease",
    "stomach","chest","body","weakness","blood","pressure",
    "diarrhea","fatigue","sore","throat","dizziness"
]

def is_health_query(message: str) -> bool:
    message = message.lower()
    return any(word in message for word in health_keywords)


app = FastAPI(title="HealthLens AI")

# ✅ CORS FIX (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production me domain daalna
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        # 1️⃣ Input safety
        safe_message = guard_user_input(request.message)

        # 👋 Greeting handling
        if is_greeting(safe_message) and not is_health_query(safe_message):
            return {
                "reply": {
                    "analysis": "Hello! I'm HealthLens AI. Please describe your symptoms so I can help analyze them.",
                    "possible_conditions": [],
                    "risk_level": "",
                    "medicine_info": [],
                    "advice": "Tell me what symptoms you are experiencing."
                },
                "disclaimer": "HealthLens AI is a health assistant, not a doctor."
            }

        # 🔒 Health-only restriction
        if not is_health_query(safe_message):
            return {
                "reply": {
                    "analysis": "I can only assist with health-related symptoms.",
                    "possible_conditions": [],
                    "risk_level": "",
                    "medicine_info": [],
                    "advice": "Please describe your health symptoms."
                },
                "disclaimer": "HealthLens AI is a health assistant, not a doctor."
            }

        # 2️⃣ AI core pipeline
        reply = run_ai_pipeline(safe_message)

        # 3️⃣ Final response
        return {
            "reply": reply,
            "disclaimer": "HealthLens AI is a health assistant, not a doctor."
        }

    except Exception as e:
        print("INTERNAL ERROR:", repr(e))
        raise HTTPException(
            status_code=500,
            detail="HealthLens AI is temporarily unavailable."
        )