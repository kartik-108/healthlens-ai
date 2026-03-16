from core.ai_core import chat

while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break

    result = chat(user_input)
    print("\nAI OUTPUT:")
    print(result)