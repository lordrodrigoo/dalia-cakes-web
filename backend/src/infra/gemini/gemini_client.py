import httpx

_GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class GeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model

    def send_message(self, message: str, history: list[dict], system_prompt: str) -> str:
        url = _GEMINI_URL.format(model=self.model)
        contents = history + [{"role": "user", "parts": [{"text": message}]}]

        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 500,
            },
        }

        response = httpx.post(
            url,
            json=payload,
            params={"key": self.api_key},
            timeout=15.0,
        )
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
