"""
Member 4 Service: Behavioral Intelligence & Multimodal Fusion Engine

Main application entry point for the microservice.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import numpy as np
from contextlib import asynccontextmanager

# ✅ FIXED IMPORTS (absolute, stable)
from api.routes import router
import api.routes as routes

from models.autoencoder import BehavioralAutoencoder
from models.anomaly import BehavioralAnomalyDetector
from core.fusion_logic import MultimodalFusionEngine, FusionWeights
from core.feature_processing import FeatureValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_synthetic_baseline_data(n_samples: int = 100) -> np.ndarray:
    """
    Generate synthetic baseline behavioral data for initial training.
    """
    np.random.seed(42)

    baseline = np.array([
        np.random.normal(3.5, 0.5, n_samples),    # typing_speed
        np.random.normal(0.15, 0.05, n_samples),  # error_rate
        np.random.normal(0.25, 0.08, n_samples),  # backspace_frequency
        np.random.normal(1.0, 0.3, n_samples),    # pause_variability
        np.random.normal(7.0, 0.8, n_samples),    # sleep_duration
        np.random.normal(0.0, 0.5, n_samples),    # sleep_drift
        np.random.normal(2.5, 0.4, n_samples),    # app_usage_entropy
        np.random.normal(15.0, 3.0, n_samples),   # session_frequency
        np.random.normal(0.75, 0.1, n_samples),   # activity_regularity
    ]).T

    baseline = np.clip(baseline, 0.0, None)
    baseline[:, 1] = np.clip(baseline[:, 1], 0.0, 1.0)
    baseline[:, 2] = np.clip(baseline[:, 2], 0.0, 1.0)
    baseline[:, 4] = np.clip(baseline[:, 4], 0.0, 24.0)
    baseline[:, 5] = np.clip(baseline[:, 5], -12.0, 12.0)
    baseline[:, 8] = np.clip(baseline[:, 8], 0.0, 1.0)

    return baseline


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / Shutdown lifecycle."""

    logger.info("Initializing Member 4 Service")

    # Initialize models
    autoencoder = BehavioralAutoencoder(input_dim=9)

    detector = BehavioralAnomalyDetector(
        autoencoder_model=autoencoder,
        anomaly_threshold=0.65
    )

    baseline_data = generate_synthetic_baseline_data(n_samples=200)

    detector.fit_baseline(baseline_data, epochs=30, verbose=False)

    fusion_weights = FusionWeights(
        sentiment_weight=0.35,
        voice_weight=0.30,
        behavioral_weight=0.35
    )

    fusion = MultimodalFusionEngine(weights=fusion_weights)

    validator = FeatureValidator()

    # ✅ SAFE GLOBAL ASSIGNMENT
    routes.anomaly_detector = detector
    routes.fusion_engine = fusion
    routes.feature_validator = validator

    logger.info("Member 4 Service Ready")

    yield

    logger.info("Shutting down Member 4 Service")


# Create FastAPI application
app = FastAPI(
    title="Member 4: Behavioral Intelligence & Multimodal Fusion Engine",
    description=(
        "Microservice for behavioral anomaly detection and multimodal risk fusion."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ FIXED ROUTER USAGE
app.include_router(router, prefix="/api/v1", tags=["Member 4"])


@app.get("/")
async def root():
    return {
        "service": "Member 4: Behavioral Intelligence & Multimodal Fusion Engine",
        "status": "operational",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8004,
        reload=True,
        log_level="info"
    )
