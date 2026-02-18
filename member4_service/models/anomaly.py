"""
Behavioral Anomaly Detection System

This module implements the core anomaly detection logic, combining
autoencoder-based reconstruction error with interpretable sub-scores
for behavioral risk assessment.
"""

import numpy as np
import torch
from typing import Dict, Tuple, Optional
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import logging

from .autoencoder import BehavioralAutoencoder, AutoencoderTrainer

logger = logging.getLogger(__name__)


class BehavioralAnomalyDetector:
    """
    Main anomaly detection engine for behavioral intelligence.
    
    Combines:
    1. Autoencoder reconstruction error (primary signal)
    2. Isolation Forest (secondary/backup detector)
    3. Interpretable sub-score analysis
    """
    
    def __init__(
        self,
        autoencoder_model: Optional[BehavioralAutoencoder] = None,
        anomaly_threshold: float = 0.05,
        device: str = 'cpu'
    ):
        """
        Initialize the anomaly detector.
        
        Args:
            autoencoder_model: Pre-trained autoencoder (or None to create new)
            anomaly_threshold: Threshold for anomaly classification
            device: Compute device ('cpu' or 'cuda')
        """
        self.device = device
        self.anomaly_threshold = anomaly_threshold
        
        # Initialize or use provided autoencoder
        if autoencoder_model is None:
            self.autoencoder = BehavioralAutoencoder(input_dim=9)
        else:
            self.autoencoder = autoencoder_model
            
        self.autoencoder.to(device)
        self.autoencoder.eval()
        
        # Initialize backup detector
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=42,
            n_estimators=100
        )
        
        # Track statistics for normalization
        self.baseline_mean = None
        self.baseline_std = None
        self.baseline_reconstruction_errors = []
        self.is_trained = False
        
        # Feature indices for sub-score computation
        self.feature_names = [
            'typing_speed', 'error_rate', 'backspace_frequency',
            'pause_variability', 'sleep_duration', 'sleep_drift',
            'app_usage_entropy', 'session_frequency', 'activity_regularity'
        ]
        
    def fit_baseline(
        self,
        baseline_data: np.ndarray,
        epochs: int = 50,
        verbose: bool = True
    ):
        """
        Train the detector on baseline behavioral data.
        
        Args:
            baseline_data: Normal behavioral patterns (N x 9 array)
            epochs: Training epochs for autoencoder
            verbose: Print training progress
        """
        logger.info(f"Training on {baseline_data.shape[0]} baseline samples")
        
        # Compute baseline statistics
        self.baseline_mean = np.mean(baseline_data, axis=0)
        self.baseline_std = np.std(baseline_data, axis=0) + 1e-8
        
        # Normalize data
        normalized_data = (baseline_data - self.baseline_mean) / self.baseline_std
        
        # Train autoencoder
        trainer = AutoencoderTrainer(
            self.autoencoder,
            learning_rate=0.001,
            device=self.device
        )
        trainer.train(normalized_data, epochs=epochs, verbose=verbose)
        
        # Compute baseline reconstruction errors
        self.baseline_reconstruction_errors = trainer.compute_reconstruction_error(
            normalized_data
        )
        
        # Train isolation forest as backup
        self.isolation_forest.fit(normalized_data)
        
        self.is_trained = True
        logger.info("Baseline training completed")
        
    def _normalize_features(self, features: np.ndarray) -> np.ndarray:
        """
        Normalize features using baseline statistics.
        
        Args:
            features: Raw feature array
            
        Returns:
            Normalized features
        """
        if self.baseline_mean is None or self.baseline_std is None:
            logger.warning("Detector not trained, using identity normalization")
            return features
            
        return (features - self.baseline_mean) / self.baseline_std
    
    def compute_reconstruction_error(self, features: np.ndarray) -> float:
        """
        Compute reconstruction error using autoencoder.
        
        Args:
            features: Normalized behavioral features (9-dim)
            
        Returns:
            Reconstruction error (MSE)
        """
        self.autoencoder.eval()
        
        with torch.no_grad():
            x = torch.FloatTensor(features).unsqueeze(0).to(self.device)
            reconstruction = self.autoencoder(x)
            error = torch.mean((x - reconstruction) ** 2).item()
            
        return error
    
    def compute_anomaly_score(self, reconstruction_error: float) -> float:
        """
        Convert reconstruction error to anomaly score [0, 1].
        
        Uses percentile-based scoring relative to baseline errors.
        
        Args:
            reconstruction_error: Raw reconstruction error
            
        Returns:
            Anomaly score in [0, 1]
        """
        if len(self.baseline_reconstruction_errors) == 0:
            # No baseline: use direct normalization
            return min(reconstruction_error / 0.1, 1.0)
        
        # Compute percentile rank
        baseline_errors = np.array(self.baseline_reconstruction_errors)
        percentile = np.sum(baseline_errors < reconstruction_error) / len(baseline_errors)
        
        # Apply exponential scaling for high percentiles
        if percentile > 0.9:
            score = 0.7 + 0.3 * ((percentile - 0.9) / 0.1)
        elif percentile > 0.7:
            score = 0.4 + 0.3 * ((percentile - 0.7) / 0.2)
        else:
            score = percentile * 0.4 / 0.7
            
        return min(score, 1.0)
    
    def compute_subscores(
        self,
        raw_features: Dict[str, float],
        normalized_features: np.ndarray
    ) -> Dict[str, float]:
        """
        Compute interpretable sub-scores for specific behavioral dimensions.
        
        Args:
            raw_features: Original feature dictionary
            normalized_features: Normalized feature array
            
        Returns:
            Dictionary of sub-scores
        """
        subscores = {}
        
        # 1. Typing Instability (combines typing speed, error rate, backspace)
        typing_features = normalized_features[:3]
        typing_deviation = np.linalg.norm(typing_features)
        subscores['typing_instability'] = min(typing_deviation / 3.0, 1.0)
        
        # 2. Sleep Irregularity (sleep duration + drift)
        sleep_features = normalized_features[4:6]
        sleep_deviation = np.linalg.norm(sleep_features)
        subscores['sleep_irregularity'] = min(sleep_deviation / 2.0, 1.0)
        
        # 3. Usage Entropy Change (app usage entropy)
        entropy_deviation = abs(normalized_features[6])
        subscores['usage_entropy_change'] = min(entropy_deviation / 2.0, 1.0)
        
        return subscores
    
    def analyze(
        self, 
        features: Dict[str, float]
    ) -> Dict[str, any]:
        """
        Perform complete behavioral anomaly analysis.
        
        Args:
            features: Dictionary of behavioral features
            
        Returns:
            Analysis results with anomaly score and sub-scores
        """
        # Convert to array
        feature_array = np.array([
            features['typing_speed'],
            features['error_rate'],
            features['backspace_frequency'],
            features['pause_variability'],
            features['sleep_duration'],
            features['sleep_drift'],
            features['app_usage_entropy'],
            features['session_frequency'],
            features['activity_regularity']
        ])
        
        # Normalize
        normalized_features = self._normalize_features(feature_array)
        
        # Compute reconstruction error
        reconstruction_error = self.compute_reconstruction_error(normalized_features)
        
        # Convert to anomaly score
        anomaly_score = self.compute_anomaly_score(reconstruction_error)
        
        # Compute sub-scores for interpretability
        subscores = self.compute_subscores(features, normalized_features)
        
        # Use isolation forest as validation
        isolation_prediction = self.isolation_forest.predict(
            normalized_features.reshape(1, -1)
        )[0]
        
        # Risk flag: threshold-based decision
        risk_flag = (
            anomaly_score > self.anomaly_threshold or 
            isolation_prediction == -1
        )
        
        result = {
            'behavioral_anomaly_score': float(anomaly_score),
            'typing_instability': float(subscores['typing_instability']),
            'sleep_irregularity': float(subscores['sleep_irregularity']),
            'usage_entropy_change': float(subscores['usage_entropy_change']),
            'risk_flag': bool(risk_flag),
            '_debug': {
                'reconstruction_error': float(reconstruction_error),
                'isolation_forest_prediction': int(isolation_prediction)
            }
        }
        
        logger.info(f"Anomaly analysis: score={anomaly_score:.3f}, risk={risk_flag}")
        
        return result


class EnsembleAnomalyDetector:
    """
    Ensemble detector combining multiple anomaly detection methods.
    
    Provides robustness through consensus-based detection.
    """
    
    def __init__(
        self,
        primary_detector: BehavioralAnomalyDetector,
        use_ensemble: bool = True
    ):
        """
        Initialize ensemble detector.
        
        Args:
            primary_detector: Primary autoencoder-based detector
            use_ensemble: Whether to use ensemble voting
        """
        self.primary = primary_detector
        self.use_ensemble = use_ensemble
        
    def analyze(self, features: Dict[str, float]) -> Dict[str, any]:
        """
        Analyze using ensemble approach.
        
        Args:
            features: Behavioral features
            
        Returns:
            Analysis results with ensemble confidence
        """
        # Primary analysis
        result = self.primary.analyze(features)
        
        if not self.use_ensemble:
            return result
        
        # Ensemble confidence based on agreement
        autoencoder_risk = result['behavioral_anomaly_score'] > 0.5
        isolation_risk = result['_debug']['isolation_forest_prediction'] == -1
        
        # Confidence score
        agreement_count = sum([autoencoder_risk, isolation_risk])
        confidence = agreement_count / 2.0
        
        result['ensemble_confidence'] = float(confidence)
        
        return result
