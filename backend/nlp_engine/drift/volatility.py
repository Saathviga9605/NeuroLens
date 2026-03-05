"""Calculate emotional volatility from sentiment scores."""
import logging
from typing import List
import statistics

logger = logging.getLogger(__name__)


def calculate_volatility(history_scores: List[float]) -> float:
    """Calculate emotional volatility as standard deviation of scores.
    
    Higher volatility indicates more unstable/fluctuating sentiment.
    Lower volatility indicates more stable sentiment.
    
    Args:
        history_scores: List of recent sentiment scores
        
    Returns:
        Standard deviation of scores (non-negative value)
        
    Raises:
        ValueError: If history_scores is empty or has only one element
    """
    if not history_scores:
        logger.error("Cannot calculate volatility with empty scores")
        raise ValueError("history_scores cannot be empty")
    
    if len(history_scores) < 2:
        logger.warning("Volatility requires at least 2 scores, returning 0.0")
        return 0.0
    
    try:
        volatility = statistics.stdev(history_scores)
        
        logger.debug(f"Volatility calculation: scores={history_scores}, "
                    f"volatility={volatility:.4f}")
        
        return float(volatility)
        
    except Exception as e:
        logger.error(f"Volatility calculation failed: {str(e)}")
        raise ValueError(f"Volatility calculation failed: {str(e)}")
