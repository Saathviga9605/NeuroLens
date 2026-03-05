import numpy as np

WINDOW_SIZE = 5
Z_THRESHOLD = 1.5


def detect_drift(current_score, historical_sessions):
    """
    Detect drift using rolling window z-score method.

    Drift is flagged when current CSI deviates
    significantly from recent baseline.
    """

    if len(historical_sessions) < WINDOW_SIZE:
        return 0

    # Take last WINDOW_SIZE scores
    recent_scores = [
        s.csi_score for s in historical_sessions[-WINDOW_SIZE:]
        if s.csi_score is not None
    ]

    if len(recent_scores) < WINDOW_SIZE:
        return 0

    mean = np.mean(recent_scores)
    std = np.std(recent_scores)

    if std == 0:
        return 0

    z_score = abs((current_score - mean) / std)

    return 1 if z_score > Z_THRESHOLD else 0