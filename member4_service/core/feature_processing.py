"""
Feature Processing and Validation Module

Handles input validation, feature engineering, and preprocessing
for behavioral intelligence analysis.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from pydantic import BaseModel, Field, validator
import logging

logger = logging.getLogger(__name__)


class BehavioralFeatures(BaseModel):
    """
    Pydantic model for behavioral feature validation.
    
    Ensures all input features are present and within valid ranges.
    """
    
    typing_speed: float = Field(
        ..., 
        ge=0.0, 
        le=10.0,
        description="Keystrokes per second (0-10 range)"
    )
    
    error_rate: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Error rate as proportion (0-1)"
    )
    
    backspace_frequency: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Backspace usage frequency (0-1)"
    )
    
    pause_variability: float = Field(
        ..., 
        ge=0.0, 
        le=10.0,
        description="Variability in typing pauses (seconds)"
    )
    
    sleep_duration: float = Field(
        ..., 
        ge=0.0, 
        le=24.0,
        description="Sleep duration in hours (0-24)"
    )
    
    sleep_drift: float = Field(
        ..., 
        ge=-12.0, 
        le=12.0,
        description="Deviation from normal sleep schedule (hours)"
    )
    
    app_usage_entropy: float = Field(
        ..., 
        ge=0.0, 
        le=5.0,
        description="Shannon entropy of app usage distribution"
    )
    
    session_frequency: float = Field(
        ..., 
        ge=0.0, 
        le=100.0,
        description="Number of sessions per day"
    )
    
    activity_regularity: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Regularity score for daily activities (0-1)"
    )
    
    @validator('*', pre=True)
    def check_not_none(cls, v):
        """Ensure no None values."""
        if v is None:
            raise ValueError("Feature value cannot be None")
        return v
    
    def to_array(self) -> np.ndarray:
        """
        Convert features to numpy array.
        
        Returns:
            9-dimensional feature array
        """
        return np.array([
            self.typing_speed,
            self.error_rate,
            self.backspace_frequency,
            self.pause_variability,
            self.sleep_duration,
            self.sleep_drift,
            self.app_usage_entropy,
            self.session_frequency,
            self.activity_regularity
        ])
    
    def to_dict(self) -> Dict[str, float]:
        """
        Convert to dictionary.
        
        Returns:
            Dictionary of features
        """
        return {
            'typing_speed': self.typing_speed,
            'error_rate': self.error_rate,
            'backspace_frequency': self.backspace_frequency,
            'pause_variability': self.pause_variability,
            'sleep_duration': self.sleep_duration,
            'sleep_drift': self.sleep_drift,
            'app_usage_entropy': self.app_usage_entropy,
            'session_frequency': self.session_frequency,
            'activity_regularity': self.activity_regularity
        }


class FeatureValidator:
    """
    Advanced feature validation and quality assessment.
    """
    
    def __init__(self):
        """Initialize validator with quality thresholds."""
        self.quality_thresholds = {
            'min_typing_speed': 0.1,
            'max_error_rate': 0.8,
            'min_sleep_duration': 2.0,
            'max_sleep_duration': 16.0
        }
    
    def validate_feature_quality(
        self, 
        features: BehavioralFeatures
    ) -> Tuple[bool, List[str]]:
        """
        Validate feature quality and detect potential data issues.
        
        Args:
            features: Validated behavioral features
            
        Returns:
            Tuple of (is_valid, list_of_warnings)
        """
        warnings = []
        
        # Check for extreme values
        if features.typing_speed < self.quality_thresholds['min_typing_speed']:
            warnings.append("Typing speed unusually low")
        
        if features.error_rate > self.quality_thresholds['max_error_rate']:
            warnings.append("Error rate unusually high")
        
        if features.sleep_duration < self.quality_thresholds['min_sleep_duration']:
            warnings.append("Sleep duration critically low")
        
        if features.sleep_duration > self.quality_thresholds['max_sleep_duration']:
            warnings.append("Sleep duration unusually high")
        
        # Check for implausible combinations
        if features.error_rate > 0.5 and features.backspace_frequency < 0.1:
            warnings.append("High errors but low backspace usage - data inconsistency")
        
        # Check for zero variance indicators
        if features.pause_variability < 0.01:
            warnings.append("Pause variability near zero - possible sensor issue")
        
        is_valid = len(warnings) == 0
        
        if warnings:
            logger.warning(f"Feature quality issues: {warnings}")
        
        return is_valid, warnings
    
    def compute_feature_statistics(
        self,
        feature_history: List[BehavioralFeatures]
    ) -> Dict[str, Dict[str, float]]:
        """
        Compute statistics over historical features.
        
        Args:
            feature_history: List of historical feature sets
            
        Returns:
            Dictionary of statistics per feature
        """
        if not feature_history:
            return {}
        
        # Convert to array
        feature_arrays = [f.to_array() for f in feature_history]
        data_matrix = np.array(feature_arrays)
        
        feature_names = [
            'typing_speed', 'error_rate', 'backspace_frequency',
            'pause_variability', 'sleep_duration', 'sleep_drift',
            'app_usage_entropy', 'session_frequency', 'activity_regularity'
        ]
        
        statistics = {}
        for i, name in enumerate(feature_names):
            statistics[name] = {
                'mean': float(np.mean(data_matrix[:, i])),
                'std': float(np.std(data_matrix[:, i])),
                'min': float(np.min(data_matrix[:, i])),
                'max': float(np.max(data_matrix[:, i])),
                'median': float(np.median(data_matrix[:, i]))
            }
        
        return statistics


class FeatureEngineer:
    """
    Advanced feature engineering for behavioral analysis.
    """
    
    @staticmethod
    def compute_derived_features(
        features: BehavioralFeatures
    ) -> Dict[str, float]:
        """
        Compute derived features from base features.
        
        Args:
            features: Base behavioral features
            
        Returns:
            Dictionary of derived features
        """
        derived = {}
        
        # Typing consistency score
        if features.pause_variability > 0:
            typing_consistency = features.typing_speed / (1 + features.pause_variability)
        else:
            typing_consistency = features.typing_speed
        derived['typing_consistency'] = float(typing_consistency)
        
        # Sleep health score
        ideal_sleep = 7.5
        sleep_deviation = abs(features.sleep_duration - ideal_sleep)
        sleep_health = max(0, 1 - (sleep_deviation / ideal_sleep))
        derived['sleep_health'] = float(sleep_health)
        
        # Overall behavioral stability
        stability_factors = [
            1 - features.error_rate,
            features.activity_regularity,
            1 - abs(features.sleep_drift) / 12.0
        ]
        behavioral_stability = np.mean(stability_factors)
        derived['behavioral_stability'] = float(behavioral_stability)
        
        return derived
    
    @staticmethod
    def create_temporal_features(
        current_features: BehavioralFeatures,
        previous_features: Optional[BehavioralFeatures] = None
    ) -> Dict[str, float]:
        """
        Create temporal change features.
        
        Args:
            current_features: Current feature set
            previous_features: Previous feature set (if available)
            
        Returns:
            Dictionary of temporal change features
        """
        if previous_features is None:
            return {
                'typing_speed_change': 0.0,
                'sleep_duration_change': 0.0,
                'activity_change': 0.0
            }
        
        temporal = {
            'typing_speed_change': current_features.typing_speed - previous_features.typing_speed,
            'sleep_duration_change': current_features.sleep_duration - previous_features.sleep_duration,
            'activity_change': current_features.activity_regularity - previous_features.activity_regularity
        }
        
        return temporal


class FeatureNormalizer:
    """
    Normalization and scaling utilities for features.
    """
    
    def __init__(self):
        """Initialize with default normalization parameters."""
        self.normalization_params = {
            'typing_speed': {'min': 0.0, 'max': 10.0},
            'error_rate': {'min': 0.0, 'max': 1.0},
            'backspace_frequency': {'min': 0.0, 'max': 1.0},
            'pause_variability': {'min': 0.0, 'max': 10.0},
            'sleep_duration': {'min': 0.0, 'max': 24.0},
            'sleep_drift': {'min': -12.0, 'max': 12.0},
            'app_usage_entropy': {'min': 0.0, 'max': 5.0},
            'session_frequency': {'min': 0.0, 'max': 100.0},
            'activity_regularity': {'min': 0.0, 'max': 1.0}
        }
    
    def normalize_minmax(
        self, 
        features: BehavioralFeatures
    ) -> np.ndarray:
        """
        Min-max normalization to [0, 1] range.
        
        Args:
            features: Input features
            
        Returns:
            Normalized feature array
        """
        feature_dict = features.to_dict()
        normalized = []
        
        for feature_name, value in feature_dict.items():
            params = self.normalization_params[feature_name]
            min_val = params['min']
            max_val = params['max']
            
            # Handle sleep_drift which can be negative
            if min_val < 0:
                normalized_value = (value - min_val) / (max_val - min_val)
            else:
                normalized_value = value / max_val
            
            normalized.append(normalized_value)
        
        return np.array(normalized)
    
    def denormalize(
        self,
        normalized_array: np.ndarray,
        feature_names: Optional[List[str]] = None
    ) -> Dict[str, float]:
        """
        Denormalize features back to original scale.
        
        Args:
            normalized_array: Normalized feature array
            feature_names: Optional list of feature names
            
        Returns:
            Dictionary of denormalized features
        """
        if feature_names is None:
            feature_names = list(self.normalization_params.keys())
        
        denormalized = {}
        
        for i, feature_name in enumerate(feature_names):
            params = self.normalization_params[feature_name]
            min_val = params['min']
            max_val = params['max']
            
            if min_val < 0:
                original_value = normalized_array[i] * (max_val - min_val) + min_val
            else:
                original_value = normalized_array[i] * max_val
            
            denormalized[feature_name] = float(original_value)
        
        return denormalized
