from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.ml.train_risk import score_features, score_chat_text


router = APIRouter()


class RiskFeatures(BaseModel):
    attendance_rate: float = Field(ge=0.0, le=1.0)
    gpa: float = Field(ge=0.0, le=4.0)
    missed_assignments: int = Field(ge=0)


class RiskRequest(BaseModel):
    features: RiskFeatures


class RiskResponse(BaseModel):
    risk: float


@router.post("/score", response_model=RiskResponse)
async def risk_score_endpoint(body: RiskRequest) -> RiskResponse:
    try:
        risk_value = score_features(
            attendance_rate=body.features.attendance_rate,
            gpa=body.features.gpa,
            missed_assignments=body.features.missed_assignments,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return RiskResponse(risk=risk_value)


class ChatRiskRequest(BaseModel):
    message: str = Field(min_length=1)


class ChatRiskResponse(BaseModel):
    wellbeing_score: float
    recommendation: str


@router.post("/from_chat", response_model=ChatRiskResponse)
async def risk_from_chat_endpoint(body: ChatRiskRequest) -> ChatRiskResponse:
    text = body.message.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    score = score_chat_text(text)
    if score < 0.3:
        rec = (
            "Your message suggests you may be going through a difficult time. "
            "Consider reaching out to your Head of Department (HOD), counseling services, or a trusted faculty member."
        )
    elif score < 0.6:
        rec = (
            "Thanks for sharing. You might benefit from study groups, time management support, and checking in with your advisor."
        )
    else:
        rec = (
            "Great to hear positive signals. Keep up your routines and support peers. If anything changes, help is available."
        )

    return ChatRiskResponse(wellbeing_score=score, recommendation=rec)


