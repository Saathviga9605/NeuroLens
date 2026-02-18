"""
FastAPI Routes for Behavioral Intelligence & Multimodal Fusion Service

Implements REST API endpoints for:
1. Behavioral anomaly analysis
2. Multimodal risk fusion
"""

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Optional
import logging

from core.feature_processing import (
    BehavioralFeatures, 
    FeatureValidator,
    FeatureEngineer
)
from core.fusion_logic import (
    MultimodalInput,
    MultimodalFusionEngine,
    AdaptiveFusionEngine,
    FusionWeights
)
from models.anomaly import BehavioralAnomalyDetector, EnsembleAnomalyDetector
from models.autoencoder import BehavioralAutoencoder

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Global instances (will be initialized in main.py)
anomaly_detector: Optional[BehavioralAnomalyDetector] = None
fusion_engine: Optional[MultimodalFusionEngine] = None
feature_validator: Optional[FeatureValidator] = None


def get_anomaly_detector() -> BehavioralAnomalyDetector:
    """Dependency to get anomaly detector instance."""
    if anomaly_detector is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Anomaly detector not initialized"
        )
    return anomaly_detector


def get_fusion_engine() -> MultimodalFusionEngine:
    """Dependency to get fusion engine instance."""
    if fusion_engine is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Fusion engine not initialized"
        )
    return fusion_engine


def get_feature_validator() -> FeatureValidator:
    """Dependency to get feature validator instance."""
    if feature_validator is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Feature validator not initialized"
        )
    return feature_validator


@router.post(
    "/behavior/analyze",
    response_model=Dict,
    status_code=status.HTTP_200_OK,
    summary="Analyze behavioral patterns for anomalies",
    description="Detects anomalies in user behavior using autoencoder-based analysis"
)
async def analyze_behavior(
    features: BehavioralFeatures,
    detector: BehavioralAnomalyDetector = Depends(get_anomaly_detector),
    validator: FeatureValidator = Depends(get_feature_validator)
) -> Dict:
    """
    Analyze behavioral features for anomalous patterns.
    
    This endpoint processes behavioral signals including typing patterns,
    sleep metrics, and activity regularity to detect deviations from
    the user's personal baseline.
    
    Args:
        features: Behavioral feature set
        detector: Injected anomaly detector
        validator: Injected feature validator
        
    Returns:
        Analysis result with anomaly scores and risk flag
        
    Example:
        ```json
        {
            "typing_speed": 3.5,
            "error_rate": 0.15,
            "backspace_frequency": 0.25,
            "pause_variability": 1.2,
            "sleep_duration": 6.5,
            "sleep_drift": -1.5,
            "app_usage_entropy": 2.3,
            "session_frequency": 12.0,
            "activity_regularity": 0.75
        }
        ```
    """
    try:
        # Validate feature quality
        is_valid, warnings = validator.validate_feature_quality(features)
        
        if not is_valid:
            logger.warning(f"Feature quality issues detected: {warnings}")
        
        # Convert to dictionary for analysis
        feature_dict = features.to_dict()
        
        # Perform anomaly analysis
        result = detector.analyze(feature_dict)
        
        # Add warnings if any
        if warnings:
            result['warnings'] = warnings
        
        # Compute derived features for additional context
        derived_features = FeatureEngineer.compute_derived_features(features)
        result['derived_metrics'] = derived_features
        
        logger.info(
            f"Behavioral analysis completed: "
            f"anomaly_score={result['behavioral_anomaly_score']:.3f}"
        )
        
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid feature values: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error in behavioral analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error during behavioral analysis"
        )


@router.post(
    "/fusion/score",
    response_model=Dict,
    status_code=status.HTTP_200_OK,
    summary="Compute multimodal risk fusion score",
    description="Combines outputs from multiple AI engines into unified risk assessment"
)
async def compute_fusion_score(
    scores: MultimodalInput,
    fusion_strategy: str = "weighted",
    use_adaptive: bool = False,
    engine: MultimodalFusionEngine = Depends(get_fusion_engine)
) -> Dict:
    """
    Fuse multiple modality scores into overall risk assessment.
    
    This endpoint combines scores from:
    - Sentiment Drift Engine (NLP analysis)
    - Voice Stress Engine (audio analysis)
    - Behavioral Anomaly Engine (this service)
    
    Args:
        scores: Input scores from all modalities
        fusion_strategy: Strategy for fusion ("weighted", "geometric", "max_agreement")
        use_adaptive: Whether to use adaptive weight adjustment
        engine: Injected fusion engine
        
    Returns:
        Fusion result with overall risk score, alert level, and dominant factor
        
    Example:
        ```json
        {
            "sentiment_drift": 0.65,
            "voice_stress": 0.45,
            "behavioral_anomaly": 0.72
        }
        ```
    """
    try:
        # Validate fusion strategy
        valid_strategies = ["weighted", "geometric", "max_agreement"]
        if fusion_strategy not in valid_strategies:
            raise ValueError(
                f"Invalid fusion strategy. Must be one of: {valid_strategies}"
            )
        
        # Use adaptive engine if requested
        if use_adaptive and not isinstance(engine, AdaptiveFusionEngine):
            logger.info("Switching to adaptive fusion engine")
            engine = AdaptiveFusionEngine(
                weights=engine.weights,
                alert_thresholds=engine.alert_thresholds
            )
        
        # Perform fusion
        result = engine.fuse(scores, fusion_strategy=fusion_strategy)
        
        logger.info(
            f"Fusion analysis completed: "
            f"overall_score={result['overall_risk_score']:.3f}, "
            f"alert_level={result['alert_level']}"
        )
        
        return result
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in fusion analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error during fusion analysis"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint"
)
async def health_check() -> Dict:
    """
    Check service health status.
    
    Returns:
        Health status information
    """
    health_status = {
        "status": "healthy",
        "service": "Behavioral Intelligence & Multimodal Fusion Engine",
        "components": {
            "anomaly_detector": anomaly_detector is not None,
            "fusion_engine": fusion_engine is not None,
            "feature_validator": feature_validator is not None
        }
    }
    
    # Check if detector is trained
    if anomaly_detector is not None:
        health_status["detector_trained"] = anomaly_detector.is_trained
    
    return health_status


@router.get(
    "/info",
    status_code=status.HTTP_200_OK,
    summary="Service information"
)
async def service_info() -> Dict:
    """
    Get service information and capabilities.
    
    Returns:
        Service metadata
    """
    return {
        "service": "Member 4: Behavioral Intelligence & Multimodal Fusion Engine",
        "version": "1.0.0",
        "capabilities": [
            "Behavioral anomaly detection",
            "Autoencoder-based pattern learning",
            "Multimodal risk fusion",
            "Interpretable sub-score analysis",
            "Adaptive weight adjustment"
        ],
        "endpoints": {
            "POST /behavior/analyze": "Analyze behavioral patterns",
            "POST /fusion/score": "Compute multimodal risk fusion",
            "GET /health": "Health check",
            "GET /info": "Service information"
        },
        "fusion_strategies": [
            "weighted",
            "geometric",
            "max_agreement"
        ]
    }


@router.post(
    "/behavior/train",
    status_code=status.HTTP_200_OK,
    summary="Train detector on baseline data",
    description="Train the anomaly detector on user's baseline behavioral data"
)
async def train_detector(
    baseline_samples: list[BehavioralFeatures],
    epochs: int = 50,
    detector: BehavioralAnomalyDetector = Depends(get_anomaly_detector)
) -> Dict:
    """
    Train the anomaly detector on baseline data.
    
    This endpoint allows updating the detector's baseline model
    with new normal behavioral patterns.
    
    Args:
        baseline_samples: List of normal behavioral feature samples
        epochs: Training epochs for autoencoder
        detector: Injected anomaly detector
        
    Returns:
        Training status and statistics
    """
    try:
        if len(baseline_samples) < 10:
            raise ValueError("Need at least 10 baseline samples for training")
        
        # Convert to numpy array
        import numpy as np
        baseline_array = np.array([sample.to_array() for sample in baseline_samples])
        
        logger.info(f"Training detector on {len(baseline_samples)} samples")
        
        # Train detector
        detector.fit_baseline(baseline_array, epochs=epochs, verbose=True)
        
        return {
            "status": "success",
            "samples_trained": len(baseline_samples),
            "epochs": epochs,
            "message": "Detector successfully trained on baseline data"
        }
        
    except ValueError as e:
        logger.error(f"Training validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error during training: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error during training"
        )


@router.post(
    "/fusion/configure",
    status_code=status.HTTP_200_OK,
    summary="Configure fusion weights",
    description="Update the fusion engine's weights for different modalities"
)
async def configure_fusion_weights(
    sentiment_weight: float = 0.35,
    voice_weight: float = 0.30,
    behavioral_weight: float = 0.35
) -> Dict:
    """
    Configure fusion weights for different modalities.
    
    Args:
        sentiment_weight: Weight for sentiment drift (0-1)
        voice_weight: Weight for voice stress (0-1)
        behavioral_weight: Weight for behavioral anomaly (0-1)
        
    Returns:
        Updated configuration
    """
    try:
        # Validate weights
        if any(w < 0 or w > 1 for w in [sentiment_weight, voice_weight, behavioral_weight]):
            raise ValueError("All weights must be between 0 and 1")
        
        # Update global fusion engine weights
        global fusion_engine
        if fusion_engine is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Fusion engine not initialized"
            )
        
        new_weights = FusionWeights(
            sentiment_weight=sentiment_weight,
            voice_weight=voice_weight,
            behavioral_weight=behavioral_weight
        )
        
        fusion_engine.weights = new_weights
        
        logger.info(f"Updated fusion weights: {new_weights.to_dict()}")
        
        return {
            "status": "success",
            "weights": new_weights.to_dict(),
            "message": "Fusion weights updated successfully"
        }
        
    except ValueError as e:
        logger.error(f"Configuration validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error updating configuration: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error during configuration update"
        )
