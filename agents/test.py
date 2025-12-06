import requests
import uuid

API_URL = "http://127.0.0.1:8000/chat"  # Adjust if your FastAPI server is hosted elsewhere
EXIT_URL = "http://127.0.0.1:8000/exit"

# Set a fixed user ID and a unique thread ID per session
user_id = "test_user"
thread_id = str(uuid.uuid4())

print("🤖 Chatbot Test Started (type 'exit' to end)\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ["exit", "quit"]:
        break

    payload = {
        "user_id": user_id,
        "thread_id": thread_id,
        "message": user_input
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        bot_reply = response.json()["response"]
        print("Bot:", bot_reply)
    except Exception as e:
        print("❌ Error communicating with chatbot:", e)

# Call the /exit endpoint to save conversation
exit_payload = {"user_id": user_id, "thread_id": thread_id}
try:
    exit_response = requests.post(EXIT_URL, json=exit_payload)
    print("💾", exit_response.json().get("message"))
except Exception as e:
    print("❌ Error saving conversation:", e)
