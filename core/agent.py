import json

from core.prompts import SYSTEM_PROMPT
from services.groq_provider import GroqProvider
from services.memory_service import add_message, get_recent_messages
from services.persona_service import get_persona
from tools.registry import TOOL_SCHEMAS, execute_tool

MAX_TOOL_ROUNDS = 5


def _is_content_blocked(exc) -> bool:
    """Deteksi error content-blocked / 400 dari provider (mis. Agentrouter)."""
    text = str(exc).lower()
    if "content-blocked" in text or "content_blocked" in text:
        return True
    resp = getattr(exc, "response", None)
    if resp is not None:
        try:
            body = resp.text.lower()
            if resp.status_code in (400, 403) and "content" in body and "block" in body:
                return True
        except Exception:
            pass
    return False


def _looks_like_error(text: str) -> bool:
    if not text:
        return True
    low = text.lower()
    return "content-blocked" in low or "bermasalah" in low or "tidak valid" in low


class Agent:
    def __init__(self):
        self.ai = GroqProvider()
        self._current_user_id = 0

    def _run_with_tools(self, messages):
        """Jalankan percakapan dengan dukungan function-calling (tools)."""
        final = None
        for _ in range(MAX_TOOL_ROUNDS):
            msg = self.ai.chat_raw(messages, tools=TOOL_SCHEMAS)
            tool_calls = msg.get("tool_calls") or []

            if not tool_calls:
                final = msg.get("content") or "(tidak ada respons)"
                break

            messages.append(
                {
                    "role": "assistant",
                    "content": msg.get("content") or "",
                    "tool_calls": tool_calls,
                }
            )

            for tc in tool_calls:
                fn = tc.get("function", {})
                name = fn.get("name", "")
                try:
                    args = json.loads(fn.get("arguments") or "{}")
                except Exception:
                    args = {}
                result = execute_tool(name, args, self._current_user_id)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.get("id", ""),
                        "content": str(result)[:6000],
                    }
                )
        else:
            final = self.ai.chat(messages)
        return final

    def respond(self, user_id: int, user_text: str) -> str:
        self._current_user_id = user_id
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
            # Percobaan utama: dengan riwayat + tools.
            final = self._run_with_tools(messages)
        except Exception as exc:
            if _is_content_blocked(exc):
                # Fallback 1: tanpa riwayat lama & tanpa tools (system + pesan user saja).
                try:
                    final = self.ai.chat(
                        [
                            {"role": "system", "content": system},
                            {"role": "user", "content": user_text},
                        ]
                    )
                except Exception:
                    final = None

                # Fallback 2: pesan paling polos tanpa system prompt sama sekali.
                if not final or _looks_like_error(final):
                    try:
                        final = self.ai.chat([{"role": "user", "content": user_text}])
                    except Exception as exc2:
                        final = self.ai._friendly_error(exc2)
            else:
                final = self.ai._friendly_error(exc)

        if not final:
            final = "(tidak ada respons)"

        add_message(user_id, "user", user_text)
        add_message(user_id, "assistant", final)
        return final
