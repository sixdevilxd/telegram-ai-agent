import base64
import mimetypes

import httpx

from config import GROQ_API_KEY, GROQ_MODEL, GROQ_VISION_MODEL


class GroqProvider:
    def __init__(self):
        if not GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY belum diisi di file .env")
        self.api_key = GROQ_API_KEY
        self.model = GROQ_MODEL
        self.vision_model = GROQ_VISION_MODEL
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _post(self, payload):
        with httpx.Client(timeout=90) as client:
            response = client.post(self.url, headers=self._headers(), json=payload)
            response.raise_for_status()
            return response.json()

    def chat(self, messages):
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024,
        }
        data = self._post(payload)
        return data["choices"][0]["message"]["content"]

    def vision(self, image_path: str, prompt: str = "Jelaskan isi gambar ini secara detail dalam bahasa Indonesia."):
        mime_type = mimetypes.guess_type(image_path)[0] or "image/jpeg"
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "model": self.vision_model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{b64}"
                            },
                        },
                    ],
                }
            ],
            "temperature": 0.2,
            "max_tokens": 1200,
        }
        data = self._post(payload)
        return data["choices"][0]["message"]["content"]
