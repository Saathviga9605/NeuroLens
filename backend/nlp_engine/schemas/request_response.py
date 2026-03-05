"""Pydantic schemas for API request and response models."""
from pydantic import BaseModel, Field, field_validator
from typing import List


class NLPAnalysisRequest(BaseModel):
    """Request schema for NLP analysis endpoint."""
    
    text: str = Field(..., min_length=1, description="Current text sample to analyze")
    history_scores: List[float] = Field(..., min_items=1, description="Recent sentiment scores")
    previous_scores: List[float] = Field(..., min_items=1, description="Earlier sentiment scores for comparison")
    
    @field_validator('text')
    @classmethod
    def validate_text_not_empty(cls, v: str) -> str:
        """Ensure text is not just whitespace."""
        if not v.strip():
            raise ValueError("Text cannot be empty or whitespace only")
        return v
    
    @field_validator('history_scores', 'previous_scores')
    @classmethod
    def validate_scores_range(cls, v: List[float]) -> List[float]:
        """Ensure all scores are in valid range [-1, 1]."""
        for score in v:
            if not -1.0 <= score <= 1.0:
                raise ValueError(f"Score {score} is out of valid range [-1, 1]")
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "I am feeling much better today after a good night's sleep.",
                    "history_scores": [0.2, 0.1, -0.05, 0.0],
                    "previous_scores": [0.4, 0.35, 0.3, 0.25]
                }
            ]
        }
    }


class NLPAnalysisResponse(BaseModel):
    """Response schema for NLP analysis endpoint."""
    
    sentiment_score: float = Field(..., description="Current sentiment score [-1, +1]")
    sentiment_drift: float = Field(..., description="Drift in sentiment over time")
    emotional_volatility: float = Field(..., description="Standard deviation of recent scores")
    linguistic_stability: float = Field(..., description="Linguistic consistency score [0, 1]")
    risk_flag: bool = Field(..., description="True if drift < -0.15 OR volatility > 0.5")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sentiment_score": 0.62,
                    "sentiment_drift": -0.18,
                    "emotional_volatility": 0.21,
                    "linguistic_stability": 0.74,
                    "risk_flag": True
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Error response schema."""
    
    error: str = Field(..., description="Error message")
    detail: str = Field(default="", description="Additional error details")
