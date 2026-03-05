from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "online",
        "service": "NeuroLens Voice Analysis API",
        "member": "Member 3 — Voice & Paralinguistic Analysis",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": [
            "POST /api/voice/analyze",
            "POST /api/voice/baseline/update",
            "GET  /api/voice/baseline/status",
            "GET  /api/voice/history",
        ]
    }
