"""
Detects English / Hindi / Telugu. langdetect struggles on very short or
code-mixed strings (common in scam SMS, e.g. "Aapka KYC block ho jayega"),
so we back it up with a raw Unicode script-range check, which is far more
reliable for Devanagari (Hindi) and Telugu script even in a two-word message.
"""
from langdetect import detect, LangDetectException

DEVANAGARI_RANGE = (0x0900, 0x097F)
TELUGU_RANGE = (0x0C00, 0x0C7F)


def _script_hint(text: str) -> str | None:
    for ch in text:
        code = ord(ch)
        if DEVANAGARI_RANGE[0] <= code <= DEVANAGARI_RANGE[1]:
            return "hi"
        if TELUGU_RANGE[0] <= code <= TELUGU_RANGE[1]:
            return "te"
    return None


def detect_language(text: str) -> str:
    """
    Returns 'en', 'hi', or 'te'. Falls back to 'en' if genuinely ambiguous
    (romanized Hindi/Telugu without native script is treated as English for
    the heuristic layer, but the LLM prompt still handles it contextually).
    """
    script_hit = _script_hint(text)
    if script_hit:
        return script_hit

    try:
        lang = detect(text)
    except LangDetectException:
        return "en"

    if lang in ("hi", "te"):
        return lang
    return "en"
