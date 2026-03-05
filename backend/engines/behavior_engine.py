import numpy as np


def normalize(value, min_val, max_val):
    """
    Normalize value safely between 0 and 1.
    """
    if max_val == min_val:
        return 0
    return max(0, min(1, (value - min_val) / (max_val - min_val)))


def calculate_behavioral_score(data, historical_sessions=None):
    """
    Behavioral Stability Score (0–100)

    Components:
    - Sleep stability
    - Typing speed (WPM)
    - Accuracy (error rate)
    - Rhythm variability (soft penalty)

    Weighted fusion approach.
    """

    sleep = data.get("sleep_hours", 0)
    wpm = data.get("wpm", 0)
    error_rate = data.get("error_rate", 0)
    rhythm_std = data.get("rhythm_std", 0)

    # -------------------------
    # 1️⃣ Sleep Score (35%)
    # Ideal around 7–8 hrs
    # Smooth deviation curve
    # -------------------------
    ideal_sleep = 7.5
    sleep_deviation = abs(sleep - ideal_sleep)
    sleep_score = max(0, 1 - (sleep_deviation / 5))  # gentle decay

    # -------------------------
    # 2️⃣ Typing Speed (35%)
    # Expected normal range: 20–80 WPM
    # -------------------------
    wpm_norm = normalize(wpm, 20, 45)

    # -------------------------
    # 3️⃣ Accuracy (20%)
    # Lower error_rate = better
    # error_rate is between 0 and 1
    # -------------------------
    accuracy_score = 1 - min(max(error_rate, 0), 1)

    # -------------------------
    # 4️⃣ Rhythm Consistency (10%)
    # Humans naturally pause.
    # Use very soft penalty.
    # Typical realistic range: 300–2000 ms
    # -------------------------
    rhythm_norm = 1 - normalize(rhythm_std, 300, 2000)

    # -------------------------
    # Weighted Fusion
    # -------------------------
    behavioral_score = (
        0.35 * sleep_score +
        0.35 * wpm_norm +
        0.20 * accuracy_score +
        0.10 * rhythm_norm
    )

    final_score = round(behavioral_score * 100, 2)

    return final_score