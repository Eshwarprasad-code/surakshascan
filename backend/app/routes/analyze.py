import logging
from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.detection_pipeline import run_detection

logger = logging.getLogger("surakshascan")
router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_message(payload: AnalyzeRequest):
    try:
        return await run_detection(payload.message)
    except Exception as exc:  # noqa: BLE001 — logged in full, returned as a clean 502 for the frontend
        logger.exception("Detection pipeline failed for a request")
        raise HTTPException(status_code=502, detail=f"Detection failed: {exc}") from exc