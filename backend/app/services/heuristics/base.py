"""
Strategy pattern: every language implements the same interface, so the
pipeline (see services/detection_pipeline.py) never needs to know which
language it's scoring. Adding a 4th language later means adding one new
class here — nothing else in the codebase changes.
"""
from abc import ABC, abstractmethod
import re

URL_PATTERN = re.compile(r"https?://\S+|www\.\S+|bit\.ly/\S+")
# Indian mobile numbers: optional +91/91 prefix, then a 10-digit number
PHONE_PATTERN = re.compile(r"(?:\+91[\-\s]?|91[\-\s]?|0)?[6-9]\d{9}\b")
UPI_ID_PATTERN = re.compile(r"\b[\w.\-]{2,}@[a-zA-Z]{2,}\b")


class ScamHeuristicStrategy(ABC):
    """One instance per detected language."""

    category_keywords: dict[str, list[str]] = {}
    urgency_keywords: list[str] = []

    def score(self, text: str) -> tuple[int, list[str], str | None]:
        """
        Returns (heuristic_score 0-60, flags, best_guess_category).
        Score is capped at 60 because the LLM layer contributes the rest —
        heuristics catch known patterns fast, the LLM catches novel wording.
        """
        flags: list[str] = []
        score = 0
        lower_text = text.lower()

        if URL_PATTERN.search(text):
            flags.append("Contains a link")
            score += 15

        if PHONE_PATTERN.search(text):
            flags.append("Contains a phone number")
            score += 5

        if UPI_ID_PATTERN.search(text):
            flags.append("Contains a UPI-style ID")
            score += 10

        matched_category = None
        best_hits = 0
        for category, keywords in self.category_keywords.items():
            hits = sum(1 for kw in keywords if kw.lower() in lower_text)
            if hits > best_hits:
                best_hits = hits
                matched_category = category
        if matched_category:
            flags.append(f"Language matches known '{matched_category}' scam pattern")
            score += min(20, best_hits * 7)

        urgency_hits = sum(1 for kw in self.urgency_keywords if kw.lower() in lower_text)
        if urgency_hits:
            flags.append("Uses urgency/threat language")
            score += min(15, urgency_hits * 5)

        return min(score, 60), flags, matched_category

    @property
    @abstractmethod
    def language_code(self) -> str:
        ...
