import httpx

from config import GROQ_API_KEY, GROQ_MODEL


class GroqProvider:
    def __init__(self):
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY belum diisi di file .env")
        self.api_key = GROQ_API_KEY
        self.model = GROQ_MODEL
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def chat(self, messages):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024,
        }

        with httpx.Client(timeout=60) as client:
            response = client.post(self.url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        return data["choices"][0]["message"]["content"]
