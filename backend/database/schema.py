from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from database.db import Base


class SessionRecord(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sleep_hours = Column(Float)
    wpm = Column(Float)
    error_rate = Column(Float)
    rhythm_std = Column(Float)

    behavioral_score = Column(Float)
    voice_score = Column(Float, nullable=True)
    nlp_score = Column(Float, nullable=True)

    csi_score = Column(Float)
    drift_flag = Column(Integer)
    risk_flag = Column(Integer)