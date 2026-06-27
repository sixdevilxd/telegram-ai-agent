import base64
import json
import mimetypes
import re
import time

import httpx

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    GROQ_VISION_MODEL,
    LLM_PROVIDER,
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    OPENROUTER_VISION_MODEL,
    AGENTROUTER_API_KEY,
    AGENTROUTER_BASE_URL,
    AGENTROUTER_MODEL,
)


class GroqProvider:
    """Provider LLM yang mendukung Groq dan OpenRouter (keduanya OpenAI-compatible)."""

    def __init__(self):
        if LLM_PROVIDER == "agentrouter":
            if not AGENTROUTER_API_KEY:
                raise RuntimeError("AGENTROUTER_API_KEY belum diisi di file .env")
            self.provider = "agentrouter"
            self.api_key = AGENTROUTER_API_KEY
            self.model = AGENTROUTER_MODEL
            self.vision_model = AGENTROUTER_MODEL
            self.url = AGENTROUTER_BASE_URL
            self.extra_headers = {}
            self._model_env = "AGENTROUTER_MODEL"
            self._key_env = "AGENTROUTER_API_KEY"
        elif LLM_PROVIDER == "openrouter":
            if not OPENROUTER_API_KEY:
                raise RuntimeError("OPENROUTER_API_KEY belum diisi di file .env")
            self.provider = "openrouter"
            self.api_key = OPENROUTER_API_KEY
            self.model = OPENROUTER_MODEL
            self.vision_model = OPENROUTER_VISION_MODEL or OPENROUTER_MODEL
            self.url = "https://openrouter.ai/api/v1/chat/completions"
            self.extra_headers = {
                "HTTP-Referer": "https://github.com/sixdevilxd/telegram-ai-agent",
                "X-Title": "Telegram AI Agent",
            }
            self._model_env = "OPENROUTER_MODEL"
            self._key_env = "OPENROUTER_API_KEY"
        else:
            if not GROQ_API_KEY:
                raise RuntimeError("GROQ_API_KEY belum diisi di file .env")
            self.provider = "groq"
            self.api_key = GROQ_API_KEY
            self.model = GROQ_MODEL
            self.vision_model = GROQ_VISION_MODEL
            self.url = "https://api.groq.com/openai/v1/chat/completions"
            self.extra_headers = {}
            self._model_env = "GROQ_MODEL"
            self._key_env = "GROQ_API_KEY"

    def _headers(self):
        h = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        h.update(self.extra_headers)
        return h

    def _post(self, payload, max_retries=3):
        """POST dengan retry + backoff untuk 429/5xx (hormati header Retry-After)."""
        last = None
        with httpx.Client(timeout=120) as client:
            for attempt in range(max_retries):
                try:
                    response = client.post(self.url, headers=self._headers(), json=payload)
                except httpx.RequestError as exc:
                    last = exc
                    if attempt < max_retries - 1:
                        time.sleep(min(2 ** attempt, 20))
                        continue
                    raise

                if response.status_code in (429, 500, 502, 503, 504):
                    last = httpx.HTTPStatusError(
                        f"HTTP {response.status_code}", request=response.request, response=response
                    )
                    if attempt < max_retries - 1:
                        retry_after = response.headers.get("retry-after")
                        try:
                            wait = float(retry_after) if retry_after else (2 ** attempt)
                        except (TypeError, ValueError):
                            wait = 2 ** attempt
                        time.sleep(min(wait, 30))
                        continue
                    raise last

                response.raise_for_status()
                return response.json()

        if last:
            raise last
        raise RuntimeError("Request LLM gagal tanpa detail.")

    def _friendly_error(self, exc) -> str:
        code = None
        if isinstance(exc, httpx.HTTPStatusError) and exc.response is not None:
            code = exc.response.status_code
        if code == 429:
            return "Bot lagi kena rate limit (429). Tunggu sebentar lalu coba lagi ya."
        if code in (401, 403):
            return f"API key tidak valid/ditolak ({code}). Cek {self._key_env} di file .env."
        if code in (404, 400):
            return (
                f"Model bermasalah (nama salah / tidak tersedia). "
                f"Cek {self._model_env} di .env. "
                "Contoh OpenRouter: anthropic/claude-sonnet-4.5 ; contoh Groq: llama-3.3-70b-versatile."
            )
        if code == 402:
            return "Saldo OpenRouter habis (402). Top-up di openrouter.ai atau pakai model gratis."
        if isinstance(exc, httpx.RequestError):
            return "Gagal terhubung ke server AI (jaringan/SSL). Coba lagi atau cek koneksi."
        return "Maaf, layanan AI sedang bermasalah. Coba lagi sebentar."

    def chat(self, messages):
        payload = {"model": self.model, "messages": messages, "temperature": 0.7, "max_tokens": 1024}
        try:
            return self._post(payload)["choices"][0]["message"]["content"]
        except Exception as exc:
            return self._friendly_error(exc)

    def chat_raw(self, messages, tools=None, tool_choice="auto"):
        """Kirim pesan + daftar tools, kembalikan objek message penuh (termasuk tool_calls)."""
        payload = {"model": self.model, "messages": messages, "temperature": 0.7, "max_tokens": 1024}
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = tool_choice
        return self._post(payload)["choices"][0]["message"]

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
        try:
            return self._post(payload)["choices"][0]["message"]["content"]
        except Exception as exc:
            return self._friendly_error(exc)

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
        try:
            raw = self._post(payload)["choices"][0]["message"]["content"]
        except Exception:
            return {}
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
