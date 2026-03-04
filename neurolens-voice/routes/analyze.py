"""
routes/analyze.py
-----------------
Voice analysis REST API endpoints.

Endpoints:
  POST /api/voice/analyze          — Analyze an audio file
  POST /api/voice/baseline/update  — Update user baseline
  GET  /api/voice/baseline/status  — Check baseline status
  GET  /api/voice/history          — Retrieve trend data
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import traceback

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.feature_extractor import VoiceFeatureExtractor
from models.stress_scorer import VoiceStressScorer
from models.baseline_manager import BaselineManager

router = APIRouter()

# Singletons (instantiated once at startup)
extractor = VoiceFeatureExtractor()
scorer = VoiceStressScorer()
baseline_mgr = BaselineManager()

SUPPORTED_FORMATS = {"audio/wav", "audio/mpeg", "audio/mp3", "audio/ogg", "audio/webm", "audio/x-wav"}


# ------------------------------------------------------------------
# POST /api/voice/analyze
# ------------------------------------------------------------------

@router.post("/analyze")
async def analyze_voice(
    file: UploadFile = File(...),
    user_id: Optional[str] = Query(default=None, description="Optional user ID for personalized scoring"),
    update_baseline: bool = Query(default=True, description="Whether to update the user's baseline with this sample")
):
    """
    Analyzes an uploaded audio file and returns voice stress scores.

    Accepts: .wav, .mp3, .ogg, .webm (browser recording)

    Returns the team API contract:
    {
        "voice_stress": 0.44,
        "speech_variability": 0.29,
        "cognitive_load_estimate": 0.51,
        "risk_flag": false,
        ...
    }
    """

    # Validate file type
    content_type = file.content_type or ""
    filename = file.filename or ""

    is_audio = (
        any(fmt in content_type for fmt in ["audio", "octet-stream"]) or
        any(filename.endswith(ext) for ext in [".wav", ".mp3", ".ogg", ".webm", ".m4a"])
    )

    if not is_audio:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {content_type}. Please upload a .wav, .mp3, or .ogg file."
        )

    # Read audio bytes
    audio_bytes = await file.read()
    if len(audio_bytes) < 1000:
        raise HTTPException(status_code=400, detail="Audio file too small or empty.")

    try:
        # Step 1: Extract raw features
        features = extractor.extract_all(audio_bytes)

        # Step 2: Get user baseline if available
        user_baseline = baseline_mgr.get_baseline(user_id) if user_id else None

        # Step 3: Score
        scores = scorer.compute_scores(features, user_baseline=user_baseline)

        # Step 4: Optionally update baseline
        baseline_info = {}
        if user_id and update_baseline:
            n_samples = baseline_mgr.update_baseline(user_id, features)
            baseline_info = baseline_mgr.baseline_status(user_id)

        # Step 5: Compose response
        response = {
            # ---- Team API contract (exact format) ----
            "voice_stress": scores["voice_stress"],
            "speech_variability": scores["speech_variability"],
            "cognitive_load_estimate": scores["cognitive_load_estimate"],
            "risk_flag": scores["risk_flag"],

            # ---- Extended data for dashboard ----
            "severity": scores["severity"],
            "sub_scores": scores["sub_scores"],
            "baseline_drift": scores["baseline_drift"],
            "baseline_info": baseline_info,

            # ---- Raw features (useful for Member 1's graphs) ----
            "raw_features": {
                "speech_rate_sps": round(features.get("speech_rate_sps", 0), 3),
                "pitch_mean_hz": round(features.get("pitch_mean_hz", 0), 2),
                "pitch_variation": round(features.get("pitch_variation", 0), 4),
                "energy_mean": round(features.get("energy_mean", 0), 5),
                "pause_ratio": round(features.get("pause_ratio", 0), 4),
                "voiced_ratio": round(features.get("voiced_ratio", 0), 4),
                "duration_seconds": round(features.get("duration_seconds", 0), 2),
            },

            # ---- Meta ----
            "user_id": user_id,
            "personalized": user_baseline is not None,
        }

        return JSONResponse(content=response)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# ------------------------------------------------------------------
# POST /api/voice/baseline/update
# ------------------------------------------------------------------

@router.post("/baseline/update")
async def update_baseline(
    file: UploadFile = File(...),
    user_id: str = Query(..., description="User ID to update baseline for")
):
    """
    Submit a 'healthy state' audio sample to build the user's personal baseline.
    Call this 3+ times when the user is known to be healthy.
    """
    audio_bytes = await file.read()

    try:
        features = extractor.extract_all(audio_bytes)
        n_samples = baseline_mgr.update_baseline(user_id, features)
        status = baseline_mgr.baseline_status(user_id)

        return {
            "message": "Baseline sample recorded.",
            "status": status,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------------------
# GET /api/voice/baseline/status
# ------------------------------------------------------------------

@router.get("/baseline/status")
async def baseline_status(user_id: str = Query(...)):
    """Check how many baseline samples have been collected for a user."""
    return baseline_mgr.baseline_status(user_id)


# ------------------------------------------------------------------
# GET /api/voice/history
# ------------------------------------------------------------------

@router.get("/history")
async def get_history(user_id: str = Query(...)):
    """
    Returns historical voice analysis samples for trend visualization.
    Useful for Member 1's sentiment drift graphs.
    """
    history = baseline_mgr.get_history(user_id)
    if not history:
        return {"user_id": user_id, "history": [], "message": "No history found."}

    # Format for charting (Member 1 can use this directly)
    chart_data = [
        {
            "timestamp": s.get("timestamp"),
            "speech_rate_sps": s.get("speech_rate_sps"),
            "pitch_variation": s.get("pitch_variation"),
            "energy_mean": s.get("energy_mean"),
            "pause_ratio": s.get("pause_ratio"),
        }
        for s in history
    ]

    return {"user_id": user_id, "history": chart_data}
