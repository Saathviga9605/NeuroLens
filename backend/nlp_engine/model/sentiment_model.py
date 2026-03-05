"""Sentiment analysis model using DistilBERT."""
import logging
from typing import Dict
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

logger = logging.getLogger(__name__)


class SentimentModel:
    """Wrapper for DistilBERT sentiment analysis model."""
    
    def __init__(self):
        """Initialize the sentiment model on startup."""
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self) -> None:
        """Load DistilBERT model and tokenizer."""
        try:
            logger.info("Loading DistilBERT sentiment model...")
            model_name = "distilbert-base-uncased-finetuned-sst-2-english"
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            
            # Create pipeline for easier inference
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1  # Use CPU (-1), or 0 for GPU
            )
            
            logger.info("DistilBERT model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load sentiment model: {str(e)}")
            raise RuntimeError(f"Model initialization failed: {str(e)}")
    
    def analyze(self, text: str) -> float:
        """Analyze sentiment of text and return score in range [-1, +1].
        
        Args:
            text: Input text to analyze
            
        Returns:
            Sentiment score normalized to [-1, +1] range
            Positive values indicate positive sentiment
            Negative values indicate negative sentiment
            
        Raises:
            ValueError: If text is empty or invalid
            RuntimeError: If model inference fails
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for sentiment analysis")
            raise ValueError("Text cannot be empty")
        
        try:
            logger.debug(f"Analyzing sentiment for text: {text[:50]}...")
            
            # Get prediction from pipeline
            result = self.pipeline(text[:512])[0]  # Limit to 512 tokens
            
            label = result['label']
            confidence = result['score']
            
            # Convert to [-1, +1] range
            # POSITIVE label -> positive score
            # NEGATIVE label -> negative score
            if label == 'POSITIVE':
                sentiment_score = confidence
            else:  # NEGATIVE
                sentiment_score = -confidence
            
            logger.debug(f"Sentiment analysis result: {sentiment_score:.4f}")
            return float(sentiment_score)
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")
            raise RuntimeError(f"Sentiment analysis failed: {str(e)}")
    
    def is_loaded(self) -> bool:
        """Check if model is loaded and ready."""
        return self.model is not None and self.tokenizer is not None


# Global singleton instance
_sentiment_model: SentimentModel = None


def get_sentiment_model() -> SentimentModel:
    """Get or create the global sentiment model instance."""
    global _sentiment_model
    if _sentiment_model is None:
        _sentiment_model = SentimentModel()
    return _sentiment_model
