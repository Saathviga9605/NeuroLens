from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.db import SessionLocal
from database.schema import SessionRecord
from engines.behavior_engine import calculate_behavioral_score
from engines.fusion_engine import calculate_csi
from drift.drift_detector import detect_drift

router = APIRouter()


class BehaviorInput(BaseModel):
    sleep_hours: float
    wpm: float
    error_rate: float
    rhythm_std: float


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/analyze")
def analyze_behavior(data: BehaviorInput, db: Session = Depends(get_db)):
    historical_sessions = db.query(SessionRecord).all()

    behavioral_score = calculate_behavioral_score(data.dict(), historical_sessions)

    # Temporary neutral scores for missing engines
    voice_score = 50
    nlp_score = 50

    csi_score = calculate_csi(behavioral_score, voice_score, nlp_score)

    drift_flag = detect_drift(csi_score, historical_sessions)

    risk_flag = 1 if csi_score > 65 else 0

    new_record = SessionRecord(
        sleep_hours=data.sleep_hours,
        wpm=data.wpm,
        error_rate=data.error_rate,
        rhythm_std=data.rhythm_std,
        behavioral_score=behavioral_score,
        voice_score=voice_score,
        nlp_score=nlp_score,
        csi_score=csi_score,
        drift_flag=drift_flag,
        risk_flag=risk_flag
    )

    db.add(new_record)
    db.commit()

    return {
        "behavioral_score": behavioral_score,
        "csi_score": csi_score,
        "drift_flag": drift_flag,
        "risk_flag": risk_flag
    }