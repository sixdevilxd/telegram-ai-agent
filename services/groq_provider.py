from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL


class GroqProvider:
    def __init__(self):
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY belum diisi di file .env")
        self.client = Groq(api_key=GROQ_API_KEY)

    def chat(self, messages):
        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content
