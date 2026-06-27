from core.prompts import SYSTEM_PROMPT
from core.tool_router import route_tool
from services.groq_provider import GroqProvider
from services.memory_service import add_message, get_recent_messages
from services.persona_service import get_persona


class Agent:
    def __init__(self):
        self.ai = GroqProvider()

    def respond(self, user_id: int, user_text: str) -> str:
        tool_result = route_tool(user_id, user_text)
        if tool_result:
            add_message(user_id, "user", user_text)
            add_message(user_id, "assistant", tool_result)
            return tool_result

        persona = get_persona(user_id)
        history = get_recent_messages(user_id)

        system = SYSTEM_PROMPT
        if persona:
            system += f"\n\nMode persona aktif: {persona}"

        messages = [{"role": "system", "content": system}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_text})

        answer = self.ai.chat(messages)

        add_message(user_id, "user", user_text)
        add_message(user_id, "assistant", answer)

        return answer
