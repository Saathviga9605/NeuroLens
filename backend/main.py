from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from contextlib import asynccontextmanager
import httpx
import logging

from api.behavior import router as behavior_router
from database.db import init_db
from api.assessment import router as assessment_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown events."""
    # Startup
    init_db()
    logger.info("NeuroLens API Gateway started on port 8000")
    logger.info("Microservices:")
    logger.info(f"  - NLP Service: {NLP_SERVICE_URL}")
    logger.info(f"  - Voice Service: {VOICE_SERVICE_URL}")
    logger.info(f"  - Member4 Service: {MEMBER4_SERVICE_URL}")
    
    yield
    
    # Shutdown
    logger.info("NeuroLens API Gateway shutting down")


app = FastAPI(
    title="NeuroLens API Gateway",
    description="Central API gateway for NeuroLens AI microservices",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS (so React frontend can call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Microservice URLs
NLP_SERVICE_URL = "http://localhost:8001"
VOICE_SERVICE_URL = "http://localhost:8002"
MEMBER4_SERVICE_URL = "http://localhost:8003"

# Include API routes
app.include_router(behavior_router, prefix="/api/behavior", tags=["Behavior"])
app.include_router(assessment_router, prefix="/api/assessment", tags=["Assessment"])


# ===== NLP Service Proxy =====

class NLPAnalyzeRequest(BaseModel):
    text: str
    history_scores: Optional[List[float]] = None
    previous_scores: Optional[List[float]] = None


@app.post("/api/nlp/analyze", tags=["NLP"])
async def proxy_nlp_analyze(request: NLPAnalyzeRequest):
    """
    Proxy endpoint for NLP sentiment analysis.
    Forwards requests to NLP microservice on port 8001.
    """
    try:
        # Provide default history if not provided
        payload = {
            "text": request.text,
            "history_scores": request.history_scores or [0.0],
            "previous_scores": request.previous_scores or [0.0]
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{NLP_SERVICE_URL}/api/nlp/analyze",
                json=payload
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"NLP service error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        logger.error(f"NLP service connection error: {e}")
        raise HTTPException(status_code=503, detail="NLP service unavailable")
    except Exception as e:
        logger.error(f"Unexpected error in NLP proxy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Voice Service Proxy =====

@app.post("/api/voice/analyze", tags=["Voice"])
async def proxy_voice_analyze(
    file: UploadFile = File(...),
    user_id: Optional[str] = Form(default=None),
    update_baseline: bool = Form(default=True)
):
    """
    Proxy endpoint for voice stress analysis.
    Forwards audio file uploads to Voice microservice on port 8002.
    """
    try:
        audio_bytes = await file.read()
        
        files = {"file": (file.filename, audio_bytes, file.content_type)}
        data = {
            "user_id": user_id,
            "update_baseline": str(update_baseline).lower()
        }
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{VOICE_SERVICE_URL}/api/voice/analyze",
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Voice service error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        logger.error(f"Voice service connection error: {e}")
        raise HTTPException(status_code=503, detail="Voice service unavailable")
    except Exception as e:
        logger.error(f"Unexpected error in Voice proxy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Member4 Fusion Service Proxy =====

@app.post("/api/fusion/score", tags=["Fusion"])
async def proxy_fusion_score(request: dict):
    """
    Proxy endpoint for multimodal fusion scoring.
    Forwards to Member4 service on port 8003.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{MEMBER4_SERVICE_URL}/api/v1/fusion/score",
                json=request
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Fusion service error: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        logger.error(f"Fusion service connection error: {e}")
        raise HTTPException(status_code=503, detail="Fusion service unavailable")
    except Exception as e:
        logger.error(f"Unexpected error in Fusion proxy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Health Check Endpoints =====

@app.get("/api/health", tags=["Health"])
async def health_check():
    """Check health of API gateway and all microservices."""
    services_status = {}
    
    # Check NLP service
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{NLP_SERVICE_URL}/health")
            services_status["nlp"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        services_status["nlp"] = "unavailable"
    
    # Check Voice service
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{VOICE_SERVICE_URL}/api/health")
            services_status["voice"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        services_status["voice"] = "unavailable"
    
    # Check Member4 service
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{MEMBER4_SERVICE_URL}/api/v1/health")
            services_status["member4"] = "healthy" if response.status_code == 200 else "unhealthy"
    except:
        services_status["member4"] = "unavailable"
    
    return {
        "gateway": "healthy",
        "services": services_status
    }


@app.get("/")
def root():
    return {
        "service": "NeuroLens API Gateway",
        "status": "operational",
        "version": "1.0.0",
        "microservices": {
            "nlp": NLP_SERVICE_URL,
            "voice": VOICE_SERVICE_URL,
            "member4": MEMBER4_SERVICE_URL
        },
        "documentation": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )