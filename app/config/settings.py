from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv(
    "GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions"
)
GROQ_API_MODEL = os.getenv(
    "GROQ_API_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"
)
