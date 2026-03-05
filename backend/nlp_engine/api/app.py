"""FastAPI application for NLP microservice."""
import logging
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from backend.nlp_engine.schemas.request_response import (
    NLPAnalysisRequest,
    NLPAnalysisResponse,
    ErrorResponse
)
from backend.nlp_engine.model.sentiment_model import get_sentiment_model
from backend.nlp_engine.drift.drift_calculator import calculate_drift
from backend.nlp_engine.drift.volatility import calculate_volatility
from backend.nlp_engine.features.linguistic_features import calculate_linguistic_stability

logger = logging.getLogger(__name__)


nlp_router = APIRouter(prefix="/nlp", tags=["NLP Analysis"])


def determine_risk_flag(drift: float, volatility: float) -> bool:
    """Determine if risk flag should be raised.
    
    Risk flag is True if:
    - sentiment_drift < -0.15 OR
    - emotional_volatility > 0.5
    
    Args:
        drift: Sentiment drift value
        volatility: Emotional volatility value
        
    Returns:
        True if risk conditions are met, False otherwise
    """
    risk = drift < -0.15 or volatility > 0.5
    
    logger.debug(f"Risk flag determination: drift={drift:.4f}, "
                f"volatility={volatility:.4f}, risk={risk}")
    
    return risk


@nlp_router.post(
    "/analyze",
    response_model=NLPAnalysisResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def analyze_nlp(request: NLPAnalysisRequest) -> NLPAnalysisResponse:
  

    logger.info(f"Received NLP analysis request for text: {request.text[:50]}...")
    
    try:
        # 1. Get sentiment model
        model = get_sentiment_model()
        
        if not model.is_loaded():
            logger.error("Sentiment model not loaded")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Model not ready"
            )
        
        # 2. Calculate sentiment score
        sentiment_score = model.analyze(request.text)
        
        
        sentiment_drift = calculate_drift(
            request.history_scores,
            request.previous_scores
        )
        
        
        emotional_volatility = calculate_volatility(request.history_scores)
        
        
        linguistic_stability = calculate_linguistic_stability(request.text)
        
        
        risk_flag = determine_risk_flag(sentiment_drift, emotional_volatility)
        
        
        response = NLPAnalysisResponse(
            sentiment_score=round(sentiment_score, 2),
            sentiment_drift=round(sentiment_drift, 2),
            emotional_volatility=round(emotional_volatility, 2),
            linguistic_stability=round(linguistic_stability, 2),
            risk_flag=risk_flag
        )
        
        logger.info(f"NLP analysis completed successfully: risk_flag={risk_flag}")
        return response
        
    except ValueError as e:
        logger.warning(f"Validation error in NLP analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input"
        )
    except Exception as e:
        logger.error(f"Unexpected error in NLP analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Analysis failed"
        )


@nlp_router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint to verify service status.
    
    Returns:
        Status message and model readiness
    """
    try:
        model = get_sentiment_model()
        model_ready = model.is_loaded()
    except Exception:
        model_ready = False
    
    return {
        "status": "healthy" if model_ready else "degraded",
        "model_loaded": model_ready
    }
