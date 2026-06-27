from core.prompts import SYSTEM_PROMPT
from services.groq_provider import GroqProvider
from services.memory_service import add_message, get_recent_messages


class Agent:
    def __init__(self):
        self.ai = GroqProvider()

    def respond(self, user_id: int, user_text: str) -> str:
        history = get_recent_messages(user_id)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_text})

        answer = self.ai.chat(messages)

        add_message(user_id, "user", user_text)
        add_message(user_id, "assistant", answer)

        return answer
