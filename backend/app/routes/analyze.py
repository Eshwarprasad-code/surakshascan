from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.detection_pipeline import run_detection

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_message(payload: AnalyzeRequest):
    try:
        return await run_detection(payload.message)
    except Exception as exc:  # noqa: BLE001 — surfaced as a clean 502 for the frontend
        raise HTTPException(status_code=502, detail=f"Detection failed: {exc}") from exc
