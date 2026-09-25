from app.services.language_detector import detect_language
from app.services.heuristics.factory import get_heuristic_strategy
from app.providers.llm_provider import get_llm_provider
from app.models.schemas import AnalyzeResponse


async def run_detection(message: str) -> AnalyzeResponse:
    # Stage 1: language detection
    language_code = detect_language(message)

    # Stage 2: heuristic scoring (fast, deterministic, works even if the
    # LLM call fails or is slow)
    strategy = get_heuristic_strategy(language_code)
    heuristic_score, heuristic_flags, heuristic_category = strategy.score(message)

    # Stage 3: LLM reasoning layer (contextual judgement + explanation)
    llm = get_llm_provider()
    llm_result = await llm.reason(message, heuristic_flags, language_code)

    # Stage 4: merge — the LLM's risk_score is the primary signal since it
    # has full context, but we nudge it up if heuristics found strong
    # pattern matches the LLM might have under-weighted.
    final_score = max(llm_result.get("risk_score", 0), heuristic_score)
    final_score = min(final_score, 100)

    if final_score >= 70:
        risk_level = "High Risk"
    elif final_score >= 35:
        risk_level = "Suspicious"
    else:
        risk_level = "Safe"

    category = llm_result.get("category") or heuristic_category or "None"

    return AnalyzeResponse(
        risk_level=risk_level,
        risk_score=final_score,
        category=category,
        language_detected=language_code,
        explanation=llm_result.get("explanation", ""),
        recommended_action=llm_result.get("recommended_action", ""),
        heuristic_flags=heuristic_flags,
    )
