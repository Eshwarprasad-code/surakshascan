import logging
from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.detection_pipeline import run_detection
from app.services.rate_limiter import get_client_ip, is_rate_limited

logger = logging.getLogger("surakshascan")
router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_message(payload: AnalyzeRequest, request: Request):
    client_ip = get_client_ip(request)
    if is_rate_limited(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many requests — please wait about a minute and try again.",
        )
    try:
        return await run_detection(payload.message)
    except Exception as exc:  # noqa: BLE001 — logged in full, returned as a clean 502 for the frontend
        logger.exception("Detection pipeline failed for a request")
        raise HTTPException(status_code=502, detail=f"Detection failed: {exc}") from exc