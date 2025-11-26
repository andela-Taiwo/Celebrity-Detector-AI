import os
import requests
from app.config import settings


class QAEngine:
    def __init__(self):
        self.groq_api_key = settings.GROQ_API_KEY
        self.groq_api_url = settings.GROQ_API_URL
        self.groq_api_model = settings.GROQ_API_MODEL
        self.temperature = 0.3
        self.max_tokens = 1024
        self.session = requests.Session()
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

    def ask_question_about_image(self, name: str, question: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json",
        }

        prompt = f"""
                    You are a AI Assistant that knows a lot about celebrities. You have to answer questions about {name} concisely and accurately.
                    Question : {question}
                    """

        payload = {
            "model": self.groq_api_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        response = requests.post(self.groq_api_url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]

        return "Sorry I couldn't find the answer"
