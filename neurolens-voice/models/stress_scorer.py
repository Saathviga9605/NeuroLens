"""
stress_scorer.py
----------------
Maps extracted audio features to interpretable mental health risk scores.

Approach:
  - Rule-based heuristics (clinically informed thresholds)
  - Anomaly scoring relative to user's personal baseline
  - Outputs normalized 0–1 scores matching the team's API contract

Clinical basis:
  - Moore et al. (2007): vocal features in depression detection
  - Cummins et al. (2015): review of depression and speech
  - Scherer et al.: paralinguistic stress markers
"""

import numpy as np
from typing import Dict, Optional


class VoiceStressScorer:
    """
    Converts raw audio features into clinical risk scores.
    Supports both baseline-free scoring and personalized baseline comparison.
    """

    def __init__(self):
        # Typical healthy speech reference ranges (population-level)
        # These are used when no personal baseline exists
        self.population_baselines = {
            "speech_rate_sps": {"mean": 4.5, "std": 0.8},       # ~4.5 syllables/sec normal
            "pitch_variation": {"mean": 0.35, "std": 0.10},      # healthy pitch variation
            "energy_mean": {"mean": 0.05, "std": 0.02},          # RMS energy
            "pause_ratio": {"mean": 0.25, "std": 0.10},          # ~25% pause is normal
            "voiced_ratio": {"mean": 0.65, "std": 0.10},         # ~65% voiced
            "zcr_std": {"mean": 0.05, "std": 0.02},              # ZCR variability
        }

    # ------------------------------------------------------------------
    # Individual risk sub-scores (all return 0.0–1.0)
    # ------------------------------------------------------------------

    def score_speech_rate(self, speech_rate_sps: float) -> float:
        """
        Very slow (<2.5 sps) or very fast (>7 sps) speech = elevated risk.
        Depression → slow. Anxiety → fast.
        Returns combined abnormality score.
        """
        if speech_rate_sps < 2.5:
            # Slow speech — depression / fatigue signal
            return np.clip(1.0 - (speech_rate_sps / 2.5), 0, 1)
        elif speech_rate_sps > 7.0:
            # Rapid speech — anxiety / mania signal
            return np.clip((speech_rate_sps - 7.0) / 3.0, 0, 1)
        else:
            # Normal range
            return 0.0

    def score_pitch_flatness(self, pitch_variation: float) -> float:
        """
        Flat pitch (low variation) = emotional numbing = depression marker.
        Healthy speech has higher pitch variation.
        """
        # Below 0.15 variation is clinically flat
        if pitch_variation < 0.15:
            return np.clip(1.0 - (pitch_variation / 0.15), 0, 1)
        return 0.0

    def score_energy_level(self, energy_mean: float, energy_flatness: float) -> float:
        """
        Low energy + flat energy pattern = low affect (depression marker).
        """
        energy_risk = np.clip(1.0 - (energy_mean / 0.08), 0, 1)
        flatness_risk = np.clip(energy_flatness, 0, 1)
        return float((energy_risk * 0.6) + (flatness_risk * 0.4))

    def score_pause_ratio(self, pause_ratio: float) -> float:
        """
        Excessive pausing (>50%) suggests word-finding difficulty or fatigue.
        """
        if pause_ratio > 0.5:
            return np.clip((pause_ratio - 0.5) / 0.5, 0, 1)
        return 0.0

    def score_vocal_stability(self, zcr_std: float) -> float:
        """
        High ZCR variability = voice tremor = anxiety/stress.
        """
        if zcr_std > 0.08:
            return np.clip((zcr_std - 0.08) / 0.10, 0, 1)
        return 0.0

    def score_mfcc_instability(self, mfcc_variance: float) -> float:
        """
        High MFCC variance = unstable vocal tract patterns = stress indicator.
        """
        # Normalize based on typical range
        return float(np.clip(mfcc_variance / 500.0, 0, 1))

    # ------------------------------------------------------------------
    # Baseline comparison (personalized scoring)
    # ------------------------------------------------------------------

    def compare_to_baseline(
        self,
        features: Dict[str, float],
        baseline: Dict[str, float]
    ) -> float:
        """
        Computes how much current features deviate from this user's personal baseline.
        Returns a drift score 0–1.
        """
        key_features = ["speech_rate_sps", "pitch_variation", "energy_mean", "pause_ratio"]
        deviations = []

        for key in key_features:
            if key in features and key in baseline:
                ref = baseline[key]
                if ref > 0:
                    deviation = abs(features[key] - ref) / (ref + 1e-6)
                    deviations.append(min(deviation, 1.0))

        return float(np.mean(deviations)) if deviations else 0.0

    # ------------------------------------------------------------------
    # Master scoring method
    # ------------------------------------------------------------------

    def compute_scores(
        self,
        features: Dict[str, float],
        user_baseline: Optional[Dict[str, float]] = None
    ) -> Dict[str, float]:
        """
        Produces the final API output scores from raw features.
        Matches team contract:
          voice_stress, speech_variability, cognitive_load_estimate, risk_flag
        """

        # --- Sub-scores ---
        speech_rate_risk = self.score_speech_rate(
            features.get("speech_rate_sps", 4.5)
        )
        pitch_flat_risk = self.score_pitch_flatness(
            features.get("pitch_variation", 0.35)
        )
        energy_risk = self.score_energy_level(
            features.get("energy_mean", 0.05),
            features.get("energy_flatness", 0.5)
        )
        pause_risk = self.score_pause_ratio(
            features.get("pause_ratio", 0.25)
        )
        vocal_stability_risk = self.score_vocal_stability(
            features.get("zcr_std", 0.05)
        )
        mfcc_risk = self.score_mfcc_instability(
            features.get("mfcc_variance", 100)
        )

        # --- Composite voice stress (weighted) ---
        # Clinical literature weights: pitch flatness and speech rate are strongest markers
        voice_stress = (
            pitch_flat_risk    * 0.30 +
            speech_rate_risk   * 0.25 +
            energy_risk        * 0.20 +
            pause_risk         * 0.15 +
            vocal_stability_risk * 0.10
        )
        voice_stress = float(np.clip(voice_stress, 0, 1))

        # --- Speech variability (inverse of stability) ---
        speech_variability = float(np.clip(
            (mfcc_risk * 0.5) + (vocal_stability_risk * 0.3) + (speech_rate_risk * 0.2),
            0, 1
        ))

        # --- Cognitive load estimate ---
        cognitive_load = float(np.clip(
            (pause_risk * 0.40) +
            (speech_rate_risk * 0.30) +
            (mfcc_risk * 0.30),
            0, 1
        ))

        # --- Baseline drift (personalized) ---
        baseline_drift = 0.0
        if user_baseline:
            baseline_drift = self.compare_to_baseline(features, user_baseline)
            # Blend drift into final scores
            voice_stress = float(np.clip(voice_stress * 0.7 + baseline_drift * 0.3, 0, 1))

        # --- Risk flag (threshold: 0.55 = moderate risk) ---
        risk_flag = voice_stress > 0.55

        # --- Severity label ---
        if voice_stress < 0.25:
            severity = "low"
        elif voice_stress < 0.55:
            severity = "moderate"
        elif voice_stress < 0.75:
            severity = "high"
        else:
            severity = "critical"

        return {
            # ---- Team API contract outputs ----
            "voice_stress": round(voice_stress, 4),
            "speech_variability": round(speech_variability, 4),
            "cognitive_load_estimate": round(cognitive_load, 4),
            "risk_flag": risk_flag,

            # ---- Extended detail (for dashboard graphs) ----
            "severity": severity,
            "sub_scores": {
                "pitch_flatness_risk": round(pitch_flat_risk, 4),
                "speech_rate_risk": round(speech_rate_risk, 4),
                "energy_risk": round(energy_risk, 4),
                "pause_risk": round(pause_risk, 4),
                "vocal_stability_risk": round(vocal_stability_risk, 4),
            },
            "baseline_drift": round(baseline_drift, 4),
        }
