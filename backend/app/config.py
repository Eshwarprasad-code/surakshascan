"""
Central config. Everything environment-specific lives here so no other
module reaches into os.environ directly.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    GROQ_API_URL: str = "https://api.groq.com/openai/v1/chat/completions"
    # Comma-separated list, e.g. "http://localhost:5173,https://surakshascan.vercel.app"
    FRONTEND_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv("FRONTEND_ORIGINS", "http://localhost:5173").split(",")
        if origin.strip()
    ]


settings = Settings()