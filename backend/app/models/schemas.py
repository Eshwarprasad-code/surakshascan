from pydantic import BaseModel, Field
from typing import Literal


class AnalyzeRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)


class AnalyzeResponse(BaseModel):
    risk_level: Literal["Safe", "Suspicious", "High Risk"]
    risk_score: int  # 0-100
    category: str
    language_detected: str
    explanation: str
    recommended_action: str
    heuristic_flags: list[str]
