"""
tests/test_pipeline.py
----------------------
Unit tests for the voice analysis pipeline.
Run with: pytest tests/test_pipeline.py -v
"""

import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.feature_extractor import VoiceFeatureExtractor
from models.stress_scorer import VoiceStressScorer
from models.baseline_manager import BaselineManager


def generate_test_audio(
    duration: float = 3.0,
    sample_rate: int = 22050,
    style: str = "normal"
) -> bytes:
    """
    Generates synthetic audio bytes for testing.
    Styles: 'normal', 'stressed', 'depressed'
    """
    import io
    import soundfile as sf

    t = np.linspace(0, duration, int(sample_rate * duration))

    if style == "normal":
        # Normal speech-like signal: varied frequency, good energy
        signal = (
            0.4 * np.sin(2 * np.pi * 150 * t) +
            0.3 * np.sin(2 * np.pi * 300 * t + np.sin(t)) +
            0.1 * np.random.randn(len(t))
        )
    elif style == "stressed":
        # Stressed: high frequency tremor, irregular energy
        signal = (
            0.3 * np.sin(2 * np.pi * 250 * t + 0.5 * np.sin(15 * t)) +
            0.2 * np.random.randn(len(t))
        )
    elif style == "depressed":
        # Depressed: low energy, flat, slow
        signal = 0.05 * np.sin(2 * np.pi * 100 * t) + 0.01 * np.random.randn(len(t))

    # Normalize
    signal = signal / (np.max(np.abs(signal)) + 1e-6) * 0.8

    # Write to bytes
    buffer = io.BytesIO()
    sf.write(buffer, signal, sample_rate, format="WAV")
    return buffer.getvalue()


class TestFeatureExtractor:
    def setup_method(self):
        self.extractor = VoiceFeatureExtractor()

    def test_extracts_all_feature_keys(self):
        audio = generate_test_audio()
        features = self.extractor.extract_all(audio)

        required_keys = [
            "mfcc_mean", "mfcc_std", "mfcc_variance",
            "pitch_mean_hz", "pitch_variation",
            "energy_mean", "energy_flatness",
            "speech_rate_sps", "duration_seconds",
            "zcr_mean", "zcr_std",
            "pause_ratio",
        ]
        for key in required_keys:
            assert key in features, f"Missing feature: {key}"

    def test_features_are_finite(self):
        audio = generate_test_audio()
        features = self.extractor.extract_all(audio)
        for k, v in features.items():
            if isinstance(v, float):
                assert np.isfinite(v), f"Feature {k} is not finite: {v}"

    def test_duration_is_approximately_correct(self):
        audio = generate_test_audio(duration=3.0)
        features = self.extractor.extract_all(audio)
        assert 2.5 <= features["duration_seconds"] <= 3.5


class TestStressScorer:
    def setup_method(self):
        self.scorer = VoiceStressScorer()

    def test_output_has_required_keys(self):
        features = {
            "speech_rate_sps": 4.5, "pitch_variation": 0.35,
            "energy_mean": 0.05, "energy_flatness": 0.4,
            "pause_ratio": 0.25, "zcr_std": 0.04, "mfcc_variance": 100
        }
        scores = self.scorer.compute_scores(features)

        required = ["voice_stress", "speech_variability", "cognitive_load_estimate", "risk_flag"]
        for key in required:
            assert key in scores, f"Missing score key: {key}"

    def test_scores_are_in_range(self):
        features = {
            "speech_rate_sps": 4.5, "pitch_variation": 0.35,
            "energy_mean": 0.05, "energy_flatness": 0.4,
            "pause_ratio": 0.25, "zcr_std": 0.04, "mfcc_variance": 100
        }
        scores = self.scorer.compute_scores(features)

        for key in ["voice_stress", "speech_variability", "cognitive_load_estimate"]:
            assert 0.0 <= scores[key] <= 1.0, f"{key} out of range: {scores[key]}"

    def test_low_energy_raises_risk(self):
        depressed_features = {
            "speech_rate_sps": 2.0,       # Slow
            "pitch_variation": 0.05,       # Flat
            "energy_mean": 0.005,          # Very low
            "energy_flatness": 0.9,        # Very flat
            "pause_ratio": 0.60,           # Lots of pauses
            "zcr_std": 0.02,
            "mfcc_variance": 50
        }
        scores = self.scorer.compute_scores(depressed_features)
        assert scores["voice_stress"] > 0.5, "Should flag depressed pattern as high stress"

    def test_normal_speech_low_risk(self):
        healthy_features = {
            "speech_rate_sps": 4.5,
            "pitch_variation": 0.40,
            "energy_mean": 0.08,
            "energy_flatness": 0.3,
            "pause_ratio": 0.20,
            "zcr_std": 0.03,
            "mfcc_variance": 80
        }
        scores = self.scorer.compute_scores(healthy_features)
        assert scores["voice_stress"] < 0.4, "Normal speech should have low stress score"

    def test_risk_flag_triggered_above_threshold(self):
        high_risk_features = {
            "speech_rate_sps": 1.5,
            "pitch_variation": 0.03,
            "energy_mean": 0.002,
            "energy_flatness": 0.95,
            "pause_ratio": 0.70,
            "zcr_std": 0.15,
            "mfcc_variance": 400
        }
        scores = self.scorer.compute_scores(high_risk_features)
        assert scores["risk_flag"] is True


class TestBaselineManager:
    def setup_method(self):
        self.mgr = BaselineManager(storage_path="/tmp/test_baselines.json")

    def test_no_baseline_before_3_samples(self):
        baseline = self.mgr.get_baseline("user_test_new")
        # New user has no baseline
        assert baseline is None or self.mgr.baseline_status("user_test_new")["samples_needed_for_baseline"] > 0

    def test_baseline_established_after_3_samples(self):
        test_user = "user_baseline_test_456"
        features = {
            "speech_rate_sps": 4.5, "pitch_mean_hz": 180,
            "pitch_variation": 0.35, "energy_mean": 0.05,
            "pause_ratio": 0.25, "voiced_ratio": 0.65,
            "zcr_mean": 0.05, "mfcc_mean": -10.0
        }
        for _ in range(3):
            self.mgr.update_baseline(test_user, features)

        status = self.mgr.baseline_status(test_user)
        assert status["baseline_ready"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
