"""
Multimodal Risk Fusion Engine

Combines outputs from multiple AI engines (sentiment, voice, behavioral)
into a unified risk assessment with interpretable alert levels.
"""

import numpy as np
from typing import Dict, Tuple, Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AlertLevel(str, Enum):
    """Risk alert levels."""
    NORMAL = "NORMAL"
    ELEVATED = "ELEVATED"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class CollapseProb(str, Enum):
    """Collapse probability categories."""
    MINIMAL = "MINIMAL"
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    SEVERE = "SEVERE"


class MultimodalInput(BaseModel):
    """
    Validated input for multimodal fusion.
    
    Receives scores from other microservices:
    - Sentiment Drift Engine (Member 1)
    - Voice Stress Engine (Member 2/3)
    - Behavioral Engine (Member 4 - this service)
    """
    
    sentiment_drift: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Sentiment drift score from NLP engine"
    )
    
    voice_stress: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Voice stress score from audio analysis"
    )
    
    behavioral_anomaly: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Behavioral anomaly score"
    )
    
    @validator('*', pre=True)
    def check_not_none(cls, v):
        """Ensure no None values."""
        if v is None:
            raise ValueError("Input score cannot be None")
        return v


class FusionWeights:
    """
    Configurable fusion weights for different modalities.
    
    Implements adaptive weighting based on reliability and signal quality.
    """
    
    def __init__(
        self,
        sentiment_weight: float = 0.35,
        voice_weight: float = 0.30,
        behavioral_weight: float = 0.35
    ):
        """
        Initialize fusion weights.
        
        Args:
            sentiment_weight: Weight for sentiment drift
            voice_weight: Weight for voice stress
            behavioral_weight: Weight for behavioral anomaly
        """
        # Normalize weights to sum to 1.0
        total = sentiment_weight + voice_weight + behavioral_weight
        
        self.sentiment = sentiment_weight / total
        self.voice = voice_weight / total
        self.behavioral = behavioral_weight / total
        
        logger.info(
            f"Fusion weights: sentiment={self.sentiment:.2f}, "
            f"voice={self.voice:.2f}, behavioral={self.behavioral:.2f}"
        )
    
    def to_dict(self) -> Dict[str, float]:
        """Return weights as dictionary."""
        return {
            'sentiment': self.sentiment,
            'voice': self.voice,
            'behavioral': self.behavioral
        }


class MultimodalFusionEngine:
    """
    Advanced multimodal fusion engine for mental health risk assessment.
    
    Implements:
    1. Weighted risk scoring
    2. Dominant factor identification
    3. Alert level classification
    4. Collapse probability estimation
    """
    
    def __init__(
        self,
        weights: Optional[FusionWeights] = None,
        alert_thresholds: Optional[Dict[str, float]] = None
    ):
        """
        Initialize fusion engine.
        
        Args:
            weights: Custom fusion weights (default: balanced)
            alert_thresholds: Custom alert thresholds
        """
        self.weights = weights or FusionWeights()
        
        # Default alert thresholds
        self.alert_thresholds = alert_thresholds or {
            'normal': 0.3,
            'elevated': 0.5,
            'high': 0.7,
            'critical': 0.85
        }
    
    def compute_weighted_score(
        self,
        scores: MultimodalInput
    ) -> float:
        """
        Compute weighted fusion score.
        
        Uses configurable weights to combine modalities.
        
        Args:
            scores: Input scores from all modalities
            
        Returns:
            Weighted overall risk score [0, 1]
        """
        weighted_score = (
            self.weights.sentiment * scores.sentiment_drift +
            self.weights.voice * scores.voice_stress +
            self.weights.behavioral * scores.behavioral_anomaly
        )
        
        return float(weighted_score)
    
    def compute_nonlinear_score(
        self,
        scores: MultimodalInput
    ) -> float:
        """
        Compute non-linear fusion score using geometric mean.
        
        More sensitive to cases where all modalities agree.
        
        Args:
            scores: Input scores from all modalities
            
        Returns:
            Non-linear risk score [0, 1]
        """
        # Geometric mean
        score_array = np.array([
            scores.sentiment_drift,
            scores.voice_stress,
            scores.behavioral_anomaly
        ])
        
        # Add small epsilon to avoid log(0)
        score_array = np.maximum(score_array, 1e-6)
        
        geometric_mean = np.exp(np.mean(np.log(score_array)))
        
        return float(geometric_mean)
    
    def compute_max_agreement_score(
        self,
        scores: MultimodalInput
    ) -> float:
        """
        Compute score emphasizing maximum agreement.
        
        Combines max score with mean to detect acute risks.
        
        Args:
            scores: Input scores from all modalities
            
        Returns:
            Max-agreement risk score [0, 1]
        """
        score_array = np.array([
            scores.sentiment_drift,
            scores.voice_stress,
            scores.behavioral_anomaly
        ])
        
        max_score = np.max(score_array)
        mean_score = np.mean(score_array)
        
        # Weight more toward max if agreement is high
        agreement_factor = 1 - np.std(score_array)
        
        combined = agreement_factor * max_score + (1 - agreement_factor) * mean_score
        
        return float(combined)
    
    def identify_dominant_factor(
        self,
        scores: MultimodalInput
    ) -> str:
        """
        Identify the dominant risk factor.
        
        Args:
            scores: Input scores from all modalities
            
        Returns:
            Name of dominant factor
        """
        score_dict = {
            'sentiment_drift': scores.sentiment_drift,
            'voice_stress': scores.voice_stress,
            'behavioral_anomaly': scores.behavioral_anomaly
        }
        
        dominant = max(score_dict.items(), key=lambda x: x[1])
        
        return dominant[0]
    
    def classify_alert_level(
        self,
        overall_score: float
    ) -> AlertLevel:
        """
        Classify alert level based on overall risk score.
        
        Args:
            overall_score: Overall risk score [0, 1]
            
        Returns:
            Alert level classification
        """
        if overall_score >= self.alert_thresholds['critical']:
            return AlertLevel.CRITICAL
        elif overall_score >= self.alert_thresholds['high']:
            return AlertLevel.HIGH
        elif overall_score >= self.alert_thresholds['elevated']:
            return AlertLevel.ELEVATED
        else:
            return AlertLevel.NORMAL
    
    def estimate_collapse_probability(
        self,
        overall_score: float,
        score_variance: float
    ) -> CollapseProb:
        """
        Estimate collapse probability category.
        
        Considers both score magnitude and variance across modalities.
        
        Args:
            overall_score: Overall risk score
            score_variance: Variance across modality scores
            
        Returns:
            Collapse probability category
        """
        # High variance indicates inconsistent signals (lower confidence)
        confidence_factor = 1.0 - min(score_variance / 0.3, 1.0)
        
        # Adjusted score considers confidence
        adjusted_score = overall_score * (0.7 + 0.3 * confidence_factor)
        
        if adjusted_score >= 0.8:
            return CollapseProb.SEVERE
        elif adjusted_score >= 0.65:
            return CollapseProb.HIGH
        elif adjusted_score >= 0.45:
            return CollapseProb.MODERATE
        elif adjusted_score >= 0.25:
            return CollapseProb.LOW
        else:
            return CollapseProb.MINIMAL
    
    def compute_risk_distribution(
        self,
        scores: MultimodalInput
    ) -> Dict[str, float]:
        """
        Compute risk contributions from each modality.
        
        Args:
            scores: Input scores from all modalities
            
        Returns:
            Dictionary of risk percentages per modality
        """
        weighted_contributions = {
            'sentiment': scores.sentiment_drift * self.weights.sentiment,
            'voice': scores.voice_stress * self.weights.voice,
            'behavioral': scores.behavioral_anomaly * self.weights.behavioral
        }
        
        total = sum(weighted_contributions.values())
        
        if total == 0:
            return {'sentiment': 0.33, 'voice': 0.33, 'behavioral': 0.34}
        
        distribution = {
            k: v / total for k, v in weighted_contributions.items()
        }
        
        return distribution
    
    def fuse(
        self,
        scores: MultimodalInput,
        fusion_strategy: str = "weighted"
    ) -> Dict[str, any]:
        """
        Perform complete multimodal fusion analysis.
        
        Args:
            scores: Input scores from all modalities
            fusion_strategy: Strategy to use ("weighted", "geometric", "max_agreement")
            
        Returns:
            Complete fusion analysis result
        """
        # Compute overall risk score using selected strategy
        if fusion_strategy == "geometric":
            overall_score = self.compute_nonlinear_score(scores)
        elif fusion_strategy == "max_agreement":
            overall_score = self.compute_max_agreement_score(scores)
        else:  # default: weighted
            overall_score = self.compute_weighted_score(scores)
        
        # Compute score variance
        score_array = np.array([
            scores.sentiment_drift,
            scores.voice_stress,
            scores.behavioral_anomaly
        ])
        score_variance = float(np.var(score_array))
        
        # Identify dominant factor
        dominant_factor = self.identify_dominant_factor(scores)
        
        # Classify alert level
        alert_level = self.classify_alert_level(overall_score)
        
        # Estimate collapse probability
        collapse_prob = self.estimate_collapse_probability(
            overall_score,
            score_variance
        )
        
        # Compute risk distribution
        risk_distribution = self.compute_risk_distribution(scores)
        
        result = {
            'overall_risk_score': float(overall_score),
            'collapse_probability': collapse_prob.value,
            'dominant_factor': dominant_factor,
            'alert_level': alert_level.value,
            '_metadata': {
                'fusion_strategy': fusion_strategy,
                'score_variance': score_variance,
                'risk_distribution': risk_distribution,
                'weights_used': self.weights.to_dict()
            }
        }
        
        logger.info(
            f"Fusion analysis: score={overall_score:.3f}, "
            f"alert={alert_level.value}, dominant={dominant_factor}"
        )
        
        return result


class AdaptiveFusionEngine(MultimodalFusionEngine):
    """
    Adaptive fusion engine that adjusts weights based on signal quality.
    
    Extends base fusion engine with dynamic weight adjustment.
    """
    
    def __init__(self, **kwargs):
        """Initialize adaptive fusion engine."""
        super().__init__(**kwargs)
        self.signal_quality_history = []
    
    def estimate_signal_quality(
        self,
        scores: MultimodalInput
    ) -> Dict[str, float]:
        """
        Estimate quality/reliability of each signal.
        
        Higher quality when scores are neither too extreme nor too flat.
        
        Args:
            scores: Input scores
            
        Returns:
            Quality estimates per modality
        """
        quality = {}
        
        for name, score in [
            ('sentiment', scores.sentiment_drift),
            ('voice', scores.voice_stress),
            ('behavioral', scores.behavioral_anomaly)
        ]:
            # Quality decreases at extremes (0 or 1) due to possible saturation
            if score < 0.05 or score > 0.95:
                quality[name] = 0.7
            else:
                quality[name] = 1.0
        
        return quality
    
    def adapt_weights(
        self,
        scores: MultimodalInput
    ) -> FusionWeights:
        """
        Adapt fusion weights based on signal quality.
        
        Args:
            scores: Input scores
            
        Returns:
            Adapted fusion weights
        """
        quality = self.estimate_signal_quality(scores)
        
        # Adjust base weights by quality
        adapted = {
            'sentiment': self.weights.sentiment * quality['sentiment'],
            'voice': self.weights.voice * quality['voice'],
            'behavioral': self.weights.behavioral * quality['behavioral']
        }
        
        # Normalize
        total = sum(adapted.values())
        
        return FusionWeights(
            sentiment_weight=adapted['sentiment'] / total,
            voice_weight=adapted['voice'] / total,
            behavioral_weight=adapted['behavioral'] / total
        )
    
    def fuse(
        self,
        scores: MultimodalInput,
        fusion_strategy: str = "weighted"
    ) -> Dict[str, any]:
        """
        Perform adaptive fusion with quality-based weight adjustment.
        
        Args:
            scores: Input scores
            fusion_strategy: Fusion strategy
            
        Returns:
            Fusion result with adapted weights
        """
        # Adapt weights
        original_weights = self.weights
        self.weights = self.adapt_weights(scores)
        
        # Perform fusion
        result = super().fuse(scores, fusion_strategy)
        
        # Add adaptation info
        result['_metadata']['adapted_weights'] = self.weights.to_dict()
        result['_metadata']['original_weights'] = original_weights.to_dict()
        
        # Restore original weights for next call
        self.weights = original_weights
        
        return result
