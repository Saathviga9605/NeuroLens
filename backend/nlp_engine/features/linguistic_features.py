"""Extract linguistic stability features from text."""
import logging
from typing import List
import statistics
import math

logger = logging.getLogger(__name__)


def calculate_lexical_diversity(text: str) -> float:
    """Calculate lexical diversity (unique words / total words).
    
    Args:
        text: Input text
        
    Returns:
        Lexical diversity score between 0 and 1
    """
    if not text or not text.strip():
        logger.warning("Empty text for lexical diversity calculation")
        return 0.0
    
    words = text.lower().split()
    if not words:
        return 0.0
    
    unique_words = len(set(words))
    total_words = len(words)
    
    diversity = unique_words / total_words
    
    logger.debug(f"Lexical diversity: {unique_words}/{total_words} = {diversity:.4f}")
    return diversity


def calculate_sentence_length_variance(text: str) -> float:
    """Calculate variance in sentence lengths.
    
    Args:
        text: Input text
        
    Returns:
        Normalized variance (lower is more stable)
    """
    if not text or not text.strip():
        logger.warning("Empty text for sentence length variance calculation")
        return 0.0
    
    # Split by common sentence delimiters
    sentences = [s.strip() for s in text.replace('!', '.').replace('?', '.').split('.') if s.strip()]
    
    if len(sentences) < 2:
        logger.debug("Less than 2 sentences, variance = 0")
        return 0.0
    
    sentence_lengths = [len(s.split()) for s in sentences]
    
    try:
        variance = statistics.variance(sentence_lengths)
        mean_length = statistics.mean(sentence_lengths)
        
        # Normalize by mean to get coefficient of variation
        if mean_length > 0:
            normalized_variance = variance / (mean_length ** 2)
        else:
            normalized_variance = 0.0
        
        logger.debug(f"Sentence length variance: {variance:.4f}, normalized: {normalized_variance:.4f}")
        return normalized_variance
        
    except Exception as e:
        logger.error(f"Sentence variance calculation failed: {str(e)}")
        return 0.0


def calculate_linguistic_stability(text: str) -> float:
    """Calculate overall linguistic stability score.
    
    Combines lexical diversity and sentence length variance into a single
    stability metric normalized to [0, 1] range.
    
    Higher scores indicate more stable/consistent language patterns.
    Lower scores indicate more erratic/inconsistent language patterns.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Linguistic stability score between 0 and 1
        
    Raises:
        ValueError: If text is empty or invalid
    """
    if not text or not text.strip():
        logger.error("Empty text for linguistic stability calculation")
        raise ValueError("Text cannot be empty")
    
    try:
        # Calculate components
        lexical_diversity = calculate_lexical_diversity(text)
        sentence_variance = calculate_sentence_length_variance(text)
        
        # Stability increases with lexical diversity
        # Stability decreases with sentence length variance
        
        # Normalize variance component (use sigmoid-like function)
        # Lower variance -> higher stability
        variance_stability = 1.0 / (1.0 + sentence_variance)
        
        # Combine: weight lexical diversity and variance stability equally
        stability = (0.5 * lexical_diversity) + (0.5 * variance_stability)
        
        # Ensure in [0, 1] range
        stability = max(0.0, min(1.0, stability))
        
        logger.debug(f"Linguistic stability: diversity={lexical_diversity:.4f}, "
                    f"variance_stability={variance_stability:.4f}, "
                    f"final_stability={stability:.4f}")
        
        return float(stability)
        
    except Exception as e:
        logger.error(f"Linguistic stability calculation failed: {str(e)}")
        raise ValueError(f"Linguistic stability calculation failed: {str(e)}")
