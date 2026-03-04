"""Calculate sentiment drift over time."""
import logging
from typing import List
import statistics

logger = logging.getLogger(__name__)


def calculate_drift(history_scores: List[float], previous_scores: List[float]) -> float:
    """Calculate sentiment drift between two time periods.
    
    Drift is calculated as: mean(history_scores) - mean(previous_scores)
    
    A negative drift indicates sentiment is declining.
    A positive drift indicates sentiment is improving.
    
    Args:
        history_scores: Recent sentiment scores
        previous_scores: Earlier sentiment scores for comparison
        
    Returns:
        Drift value (can be positive or negative)
        
    Raises:
        ValueError: If either list is empty
    """
    if not history_scores or not previous_scores:
        logger.error("Cannot calculate drift with empty score lists")
        raise ValueError("Both history_scores and previous_scores must be non-empty")
    
    try:
        history_mean = statistics.mean(history_scores)
        previous_mean = statistics.mean(previous_scores)
        
        drift = history_mean - previous_mean
        
        logger.debug(f"Drift calculation: history_mean={history_mean:.4f}, "
                    f"previous_mean={previous_mean:.4f}, drift={drift:.4f}")
        
        return float(drift)
        
    except Exception as e:
        logger.error(f"Drift calculation failed: {str(e)}")
        raise ValueError(f"Drift calculation failed: {str(e)}")
