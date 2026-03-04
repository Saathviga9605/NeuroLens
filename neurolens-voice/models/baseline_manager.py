"""
baseline_manager.py
-------------------
Manages personalized voice baselines per user.

A baseline is the user's "normal" voice profile, built from their first
few recordings when healthy. All future scores are compared against this.

Storage: JSON file (swap for MongoDB in production — just change the adapter).
"""

import json
import os
import numpy as np
from typing import Dict, Optional
from datetime import datetime

BASELINE_FILE = "data/baselines.json"


class BaselineManager:
    """
    Stores and retrieves per-user voice baselines.
    In production, replace file I/O with MongoDB calls.
    """

    TRACKED_FEATURES = [
        "speech_rate_sps",
        "pitch_mean_hz",
        "pitch_variation",
        "energy_mean",
        "pause_ratio",
        "voiced_ratio",
        "zcr_mean",
        "mfcc_mean",
    ]

    def __init__(self, storage_path: str = BASELINE_FILE):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        self._data = self._load()

    def _load(self) -> Dict:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(self.storage_path, "w") as f:
            json.dump(self._data, f, indent=2)

    def get_baseline(self, user_id: str) -> Optional[Dict[str, float]]:
        """Returns the user's baseline, or None if not yet established."""
        user = self._data.get(user_id)
        if not user or len(user.get("samples", [])) < 3:
            return None
        return user.get("baseline")

    def update_baseline(self, user_id: str, features: Dict[str, float]):
        """
        Adds a new sample and recalculates baseline (rolling average).
        Requires at least 3 samples before a baseline is considered reliable.
        """
        if user_id not in self._data:
            self._data[user_id] = {"samples": [], "baseline": {}, "created_at": datetime.utcnow().isoformat()}

        # Extract only tracked features
        sample = {k: features[k] for k in self.TRACKED_FEATURES if k in features}
        sample["timestamp"] = datetime.utcnow().isoformat()
        self._data[user_id]["samples"].append(sample)

        # Keep last 20 samples for rolling baseline
        samples = self._data[user_id]["samples"][-20:]
        self._data[user_id]["samples"] = samples

        # Recalculate baseline as mean of all samples
        if len(samples) >= 3:
            baseline = {}
            for key in self.TRACKED_FEATURES:
                values = [s[key] for s in samples if key in s]
                if values:
                    baseline[key] = float(np.mean(values))
            self._data[user_id]["baseline"] = baseline
            self._data[user_id]["baseline_updated_at"] = datetime.utcnow().isoformat()

        self._save()
        return len(samples)

    def get_history(self, user_id: str) -> list:
        """Returns all historical samples for trend visualization."""
        user = self._data.get(user_id, {})
        return user.get("samples", [])

    def baseline_status(self, user_id: str) -> Dict:
        """How many more samples are needed to establish a baseline."""
        user = self._data.get(user_id, {})
        n_samples = len(user.get("samples", []))
        needed = max(0, 3 - n_samples)
        return {
            "samples_collected": n_samples,
            "samples_needed_for_baseline": needed,
            "baseline_ready": needed == 0,
        }
