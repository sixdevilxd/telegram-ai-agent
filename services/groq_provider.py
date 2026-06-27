import base64
import json
import mimetypes
import re

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
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def _post(self, payload):
        with httpx.Client(timeout=90) as client:
            response = client.post(self.url, headers=self._headers(), json=payload)
            response.raise_for_status()
            return response.json()

    def chat(self, messages):
        payload = {"model": self.model, "messages": messages, "temperature": 0.7, "max_tokens": 1024}
        return self._post(payload)["choices"][0]["message"]["content"]

    def _image_payload_content(self, image_path, prompt):
        mime_type = mimetypes.guess_type(image_path)[0] or "image/jpeg"
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{b64}"}},
        ]

    def vision(self, image_path, prompt="Jelaskan isi gambar ini secara detail dalam bahasa Indonesia."):
        payload = {
            "model": self.vision_model,
            "messages": [{"role": "user", "content": self._image_payload_content(image_path, prompt)}],
            "temperature": 0.2,
            "max_tokens": 1200,
        }
        return self._post(payload)["choices"][0]["message"]["content"]

    def vision_structured(self, image_path):
        prompt = (
            "Analisis chart trading pada gambar ini. Jawab HANYA dalam JSON valid tanpa teks lain. "
            "Gunakan bahasa Indonesia untuk nilai teks. Jangan mengarang angka yang tidak terlihat. "
            "Skema JSON:\n"
            "{\n"
            '  "asset": "string",\n'
            '  "timeframe": "string",\n'
            '  "trend": "uptrend|downtrend|sideways",\n'
            '  "supports": ["level1", "level2"],\n'
            '  "resistances": ["level1", "level2"],\n'
            '  "pattern": "string",\n'
            '  "indicators": "string",\n'
            '  "bullish_scenario": "string",\n'
            '  "bearish_scenario": "string",\n'
            '  "bias": "bullish|bearish|netral",\n'
            '  "confidence": "rendah|sedang|tinggi",\n'
            '  "summary": "string"\n'
            "}"
        )
        payload = {
            "model": self.vision_model,
            "messages": [{"role": "user", "content": self._image_payload_content(image_path, prompt)}],
            "temperature": 0.1,
            "max_tokens": 1200,
        }
        raw = self._post(payload)["choices"][0]["message"]["content"]
        return _parse_json(raw)


def _parse_json(raw: str) -> dict:
    if not raw:
        return {}
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return {"summary": raw}
    try:
        return json.loads(match.group(0))
    except Exception:
        return {"summary": raw}
