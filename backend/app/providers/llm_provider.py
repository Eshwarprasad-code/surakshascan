"""
Factory pattern: the rest of the app depends only on LLMProvider.reason(),
never on Groq specifically. If Groq's free tier rate-limits during judging,
add a GeminiProvider class here and flip get_llm_provider() — nothing in
services/detection_pipeline.py needs to change.
"""
from abc import ABC, abstractmethod
import json
import httpx
from app.config import settings


SYSTEM_PROMPT = """You are a fraud-detection assistant specialized in Indian \
digital scams (UPI fraud, fake KYC/bank messages, courier/customs scams, \
lottery scams, job scams, "digital arrest" scams). You will be given a \
message (possibly in English, Hindi, or Telugu) plus heuristic flags \
already detected by a rule-based system. Combine your own judgement with \
those flags.

Respond with ONLY a JSON object, no other text, in exactly this shape:
{
  "risk_level": "Safe" | "Suspicious" | "High Risk",
  "risk_score": <integer 0-100>,
  "category": "<short category name, or 'None' if safe>",
  "explanation": "<2-3 plain-language sentences a non-technical person can \
understand, in the SAME language as the input message>",
  "recommended_action": "<one concrete next step, e.g. 'Do not click the \
link or share your UPI PIN. Report this to the National Cyber Crime \
Helpline at 1930 or cybercrime.gov.in.' — in the same language as the \
input message>"
}
"""


class LLMProvider(ABC):
    @abstractmethod
    async def reason(self, message: str, heuristic_flags: list[str], language_code: str) -> dict:
        ...


class GroqProvider(LLMProvider):
    async def reason(self, message: str, heuristic_flags: list[str], language_code: str) -> dict:
        user_prompt = (
            f"Language detected: {language_code}\n"
            f"Heuristic flags already found: {heuristic_flags or 'none'}\n"
            f"Message:\n\"\"\"\n{message}\n\"\"\""
        )

        payload = {
            "model": settings.GROQ_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(settings.GROQ_API_URL, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()

        raw_content = data["choices"][0]["message"]["content"]
        return json.loads(raw_content)


def get_llm_provider() -> LLMProvider:
    return GroqProvider()
