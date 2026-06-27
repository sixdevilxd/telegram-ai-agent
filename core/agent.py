import json

from core.prompts import SYSTEM_PROMPT
from services.groq_provider import GroqProvider
from services.memory_service import add_message, get_recent_messages
from services.persona_service import get_persona
from tools.registry import TOOL_SCHEMAS, execute_tool

MAX_TOOL_ROUNDS = 5


class Agent:
    def __init__(self):
        self.ai = GroqProvider()

    def respond(self, user_id: int, user_text: str) -> str:
        persona = get_persona(user_id)
        history = get_recent_messages(user_id)

        system = SYSTEM_PROMPT
        if persona:
            system += f"\n\nMode persona aktif: {persona}"

        messages = [{"role": "system", "content": system}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_text})

        final = None
        try:
            for _ in range(MAX_TOOL_ROUNDS):
                msg = self.ai.chat_raw(messages, tools=TOOL_SCHEMAS)
                tool_calls = msg.get("tool_calls") or []

                if not tool_calls:
                    final = msg.get("content") or "(tidak ada respons)"
                    break

                # Catat permintaan tool dari assistant.
                messages.append(
                    {
                        "role": "assistant",
                        "content": msg.get("content") or "",
                        "tool_calls": tool_calls,
                    }
                )

                # Eksekusi setiap tool dan kembalikan hasilnya.
                for tc in tool_calls:
                    fn = tc.get("function", {})
                    name = fn.get("name", "")
                    try:
                        args = json.loads(fn.get("arguments") or "{}")
                    except Exception:
                        args = {}
                    result = execute_tool(name, args, user_id)
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.get("id", ""),
                            "content": str(result)[:6000],
                        }
                    )
            else:
                # Ronde tool habis: minta jawaban final tanpa tool.
                final = self.ai.chat(messages)
        except Exception as exc:
            final = self.ai._friendly_error(exc)

        if not final:
            final = "(tidak ada respons)"

        add_message(user_id, "user", user_text)
        add_message(user_id, "assistant", final)
        return final
