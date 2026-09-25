from .base import ScamHeuristicStrategy
from .english import EnglishHeuristics
from .hindi import HindiHeuristics
from .telugu import TeluguHeuristics

_STRATEGIES: dict[str, ScamHeuristicStrategy] = {
    "en": EnglishHeuristics(),
    "hi": HindiHeuristics(),
    "te": TeluguHeuristics(),
}


def get_heuristic_strategy(language_code: str) -> ScamHeuristicStrategy:
    """Falls back to English if an unsupported code somehow shows up."""
    return _STRATEGIES.get(language_code, _STRATEGIES["en"])
