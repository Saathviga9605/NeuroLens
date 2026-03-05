"""
NeuroLens NLP Microservice - Standalone Launcher
Port: 8001
Endpoints: /api/nlp/*
"""
import logging
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Add backend to path for imports
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.nlp_engine.api.app import nlp_router
from backend.nlp_engine.model.sentiment_model import get_sentiment_model

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    # Startup
    logger.info("Starting NLP microservice on port 8001...")
    try:
        model = get_sentiment_model()
        logger.info(f"Sentiment model loaded: {model.is_loaded()}")
    except Exception as e:
        logger.error(f"Failed to load sentiment model: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info("NLP microservice shutting down")


# Create FastAPI app
app = FastAPI(
    title="NeuroLens NLP Microservice",
    description="Sentiment drift and linguistic analysis for mental health monitoring",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include NLP router
app.include_router(nlp_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "service": "NeuroLens NLP Microservice",
        "status": "operational",
        "version": "1.0.0",
        "port": 8001,
        "endpoints": {
            "analyze": "/api/nlp/analyze",
            "health": "/api/nlp/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    try:
        model = get_sentiment_model()
        model_ready = model.is_loaded()
    except:
        model_ready = False
    
    return {
        "status": "healthy" if model_ready else "degraded",
        "model_loaded": model_ready
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
