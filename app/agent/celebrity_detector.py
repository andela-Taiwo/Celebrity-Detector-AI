import base64
import re
from dataclasses import dataclass
from typing import Dict, Optional
import os
from groq import Groq
import requests

from app.config import settings


@dataclass
class CelebrityProfile:
    raw_response: str
    full_name: str = "Unknown"
    profession: str = "Unknown"
    nationality: str = "Unknown"
    famous_for: str = "Unknown"
    top_achievements: str = "Unknown"

    _FIELD_MAP = {
        "full_name": "Full Name",
        "profession": "Profession",
        "nationality": "Nationality",
        "famous_for": "Famous For",
        "top_achievements": "Top Achievements",
    }

    @classmethod
    def from_response(cls, response_text: str) -> "CelebrityProfile":
        if not response_text:
            return cls(raw_response="")

        kwargs = {"raw_response": response_text}
        for attr, label in cls._FIELD_MAP.items():
            kwargs[attr] = cls._extract_field(response_text, label)
        return cls(**kwargs)

    @staticmethod
    def _extract_field(response_text: str, label: str) -> str:
        pattern = re.compile(rf"-\s*\*\*{re.escape(label)}\*\*:\s*(.+)", re.IGNORECASE)
        match = pattern.search(response_text)
        if not match:
            return "Unknown"
        value = match.group(1).strip()
        return value.splitlines()[0].strip() or "Unknown"

    def is_known(self) -> bool:
        return self.full_name != "Unknown"


class CelebrityDetector:
    PROMPT_TEXT = (
        "You are a celebrity recognition expert AI.\n"
        "Identify the person in the image. If known, respond in this format:\n\n"
        "- **Full Name**:\n"
        "- **Profession**:\n"
        "- **Nationality**:\n"
        "- **Famous For**:\n"
        "- **Top Achievements**:\n\n"
        'If unknown, return "Unknown".'
    )

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 1024,
        session: Optional[requests.Session] = None,
    ):
        self.groq_api_key = api_key or settings.GROQ_API_KEY
        self.groq_api_url = api_url or settings.GROQ_API_URL
        self.groq_api_model = model or settings.GROQ_API_MODEL
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.session = session or requests.Session()
        self._validate_configuration()

    def _validate_configuration(self) -> None:
        missing = [
            name
            for name, value in {
                "GROQ_API_KEY": self.groq_api_key,
                "GROQ_API_URL": self.groq_api_url,
                "GROQ_API_MODEL": self.groq_api_model,
            }.items()
            if not value
        ]
        if missing:
            missing_str = ", ".join(missing)
            raise ValueError(f"Missing Groq configuration values: {missing_str}")

    def detect_celebrity(self, image_bytes: bytes) -> CelebrityProfile:
        payload = self._build_payload(image_bytes)
        response_json = self._send_request(payload)
        content = self._extract_response_text(response_json)
        return CelebrityProfile.from_response(content)

    def _build_payload(self, image_bytes: bytes) -> Dict:
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")
        return {
            "model": self.groq_api_model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self.PROMPT_TEXT},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            },
                        },
                    ],
                }
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

    def _send_request(self, payload: Dict) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json",
        }

        client = Groq(api_key=self.groq_api_key)
        # paylooad = s
        chat_completion = client.chat.completions.create(
            messages=payload["messages"],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        print(chat_completion.choices[0].message.content)
        response = self.session.post(
            self.groq_api_url, headers=headers, json=payload, timeout=30
        )
        # response.raise_for_status()
        print(response.json())
        return response.json()

    @staticmethod
    def _extract_response_text(response_json: Dict) -> str:
        try:
            return response_json["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            return "Unknown"
