"""
Core logic package for Member 4 Service.

Contains feature processing and multimodal fusion logic.
"""

from .feature_processing import (
    BehavioralFeatures,
    FeatureValidator,
    FeatureEngineer,
    FeatureNormalizer
)
from .fusion_logic import (
    MultimodalInput,
    MultimodalFusionEngine,
    AdaptiveFusionEngine,
    FusionWeights,
    AlertLevel,
    CollapseProb
)

__all__ = [
    'BehavioralFeatures',
    'FeatureValidator',
    'FeatureEngineer',
    'FeatureNormalizer',
    'MultimodalInput',
    'MultimodalFusionEngine',
    'AdaptiveFusionEngine',
    'FusionWeights',
    'AlertLevel',
    'CollapseProb'
]
