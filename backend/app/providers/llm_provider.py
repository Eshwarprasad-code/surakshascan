"""
Factory pattern: the rest of the app depends only on LLMProvider.reason(),
never on Groq specifically. If Groq's free tier rate-limits during judging,
add a GeminiProvider class here and flip get_llm_provider() — nothing in
services/detection_pipeline.py needs to change.
"""
from abc import ABC, abstractmethod
import asyncio
import json
import httpx
from app.config import settings

MAX_RETRIES = 3


SYSTEM_PROMPT = """You are a fraud-detection assistant specialized in Indian \
digital scams (UPI fraud, fake KYC/bank messages, courier/customs scams, \
lottery scams, job scams, "digital arrest" scams, fake account-suspension \
phishing). You will be given a message (possibly in English, Hindi, or \
Telugu) plus heuristic flags already detected by a rule-based system. \
Combine your own judgement with those flags.

Do NOT flag a message as risky just because it mentions money, a bank \
name, or contains a mild urgency phrase in isolation. Routine transaction \
notifications (e.g. "Rs 450 credited to your account", "your bank account \
has been debited") are normal, everyday, SAFE messages sent by real \
banks — only flag them if they also ask the user to click a link, share \
an OTP/PIN/password, or take an action outside of normal banking. \
Similarly, a completed-transaction confirmation (delivery, ticket \
booking, payment received) with no link and no request for personal \
information is SAFE even if it has a stray urgency word — judge the \
message as a whole, not by any single keyword.

One important exception: a message claiming money was credited "by \
mistake" or unexpectedly, which then asks the recipient to call a number, \
return the funds, or contact "support" to resolve it, IS a known real \
scam pattern (a fake-refund / accidental-credit scam) — flag this even \
though it looks like a transaction notification on the surface.

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

        last_error = None
        async with httpx.AsyncClient(timeout=15.0) as client:
            for attempt in range(MAX_RETRIES):
                resp = await client.post(settings.GROQ_API_URL, json=payload, headers=headers)
                if resp.status_code == 429:
                    # Rate limited — back off and retry rather than failing
                    # the whole request outright. Groq sends a Retry-After
                    # header when it has one; fall back to exponential
                    # backoff (1s, 2s, 4s) if it doesn't.
                    wait = float(resp.headers.get("retry-after", 2 ** attempt))
                    last_error = f"Rate limited (429), retry {attempt + 1}/{MAX_RETRIES} after {wait}s"
                    await asyncio.sleep(wait)
                    continue
                resp.raise_for_status()
                data = resp.json()
                raw_content = data["choices"][0]["message"]["content"]
                return json.loads(raw_content)

        raise RuntimeError(f"Groq API still rate-limited after {MAX_RETRIES} retries: {last_error}")


def get_llm_provider() -> LLMProvider:
    return GroqProvider()