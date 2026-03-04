from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.db import SessionLocal
from database.schema import SessionRecord

from engines.behavior_engine import calculate_behavioral_score
from engines.fusion_engine import calculate_csi
from drift.drift_detector import detect_drift

router = APIRouter()


class AssessmentInput(BaseModel):
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


@router.post("/run")
def run_assessment(data: AssessmentInput, db: Session = Depends(get_db)):

    historical_sessions = db.query(SessionRecord).all()

    # 1️⃣ Behavioral Engine
    behavioral_score = calculate_behavioral_score(data.dict(), historical_sessions)

    # 2️⃣ Placeholder Voice & NLP (for now)
    voice_score = 50
    nlp_score = 50

    # 3️⃣ Fusion Engine
    csi_score = calculate_csi(behavioral_score, voice_score, nlp_score)

    # 4️⃣ Drift Detection
    drift_flag = detect_drift(csi_score, historical_sessions)

    # 5️⃣ Risk Flag
    risk_flag = 1 if csi_score > 65 else 0

    # Save session
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
        "voice_score": voice_score,
        "nlp_score": nlp_score,
        "csi_score": csi_score,
        "drift_flag": drift_flag,
        "risk_flag": risk_flag
    }

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    sessions = db.query(SessionRecord).order_by(SessionRecord.timestamp).all()

    return [
        {
            "timestamp": session.timestamp,
            "behavioral_score": session.behavioral_score,
            "voice_score": session.voice_score,
            "nlp_score": session.nlp_score,
            "csi_score": session.csi_score,
            "drift_flag": session.drift_flag,
            "risk_flag": session.risk_flag,
        }
        for session in sessions
    ]