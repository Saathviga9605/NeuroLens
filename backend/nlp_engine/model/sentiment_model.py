"""
Sentiment analysis model with automatic fallback.
Tries DistilBERT first, falls back to TextBlob for Python 3.13 compatibility.
"""
import logging
from typing import Dict

logger = logging.getLogger(__name__)

# Try importing transformers, fall back to TextBlob if not available
TRANSFORMERS_AVAILABLE = False
TEXTBLOB_AVAILABLE = False

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
    logger.info("Transformers available - using advanced sentiment model")
except Exception as e:
    logger.warning(f"Transformers not available: {e}")
    try:
        from textblob import TextBlob
        TEXTBLOB_AVAILABLE = True
        logger.info("Using TextBlob as fallback sentiment analyzer")
    except ImportError:
        logger.warning("TextBlob not available - using basic sentiment analyzer")


class SentimentModel:
    """Wrapper for sentiment analysis with automatic fallback."""
    
    def __init__(self):
        """Initialize the sentiment model on startup."""
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.mode = None
        self._load_model()
    
    def _load_model(self) -> None:
        """Load best available sentiment model."""
        if TRANSFORMERS_AVAILABLE:
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
                
                self.mode = "transformers"
                logger.info("DistilBERT model loaded successfully")
                return
            except Exception as e:
                logger.warning(f"Failed to load transformers model, falling back: {str(e)}")
        
        # Fallback to TextBlob
        if TEXTBLOB_AVAILABLE:
            self.mode = "textblob"
            logger.info("Using TextBlob fallback model")
        else:
            self.mode = "basic"
            logger.warning("Using basic keyword-based sentiment analysis")
    
    def analyze(self, text: str) -> float:
        """Analyze sentiment of text and return score in range [-1, +1].
        
        Args:
            text: Input text to analyze
            
        Returns:
            Sentiment score normalized to [-1, +1] range
            Positive values indicate positive sentiment
            Negative values indicate negative sentiment
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for sentiment analysis")
            return 0.0  # Return neutral instead of raising error
        
        try:
            if self.mode == "transformers" and self.pipeline:
                return self._analyze_transformers(text)
            elif self.mode == "textblob":
                return self._analyze_textblob(text)
            else:
                return self._analyze_basic(text)
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")
            return 0.0  # Return neutral on error
    
    def _analyze_transformers(self, text: str) -> float:
        """Analyze using transformers model."""
        logger.debug(f"Analyzing sentiment (transformers) for text: {text[:50]}...")
        
        # Get prediction from pipeline
        result = self.pipeline(text[:512])[0]  # Limit to 512 tokens
        
        label = result['label']
        confidence = result['score']
        
        # Convert to [-1, +1] range
        if label == 'POSITIVE':
            sentiment_score = confidence
        else:  # NEGATIVE
            sentiment_score = -confidence
        
        logger.debug(f"Sentiment analysis result: {sentiment_score:.4f}")
        return float(sentiment_score)
    
    def _analyze_textblob(self, text: str) -> float:
        """Analyze using TextBlob."""
        from textblob import TextBlob
        
        logger.debug(f"Analyzing sentiment (TextBlob) for text: {text[:50]}...")
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity  # Already in [-1, 1]
        
        logger.debug(f"Sentiment analysis result: {sentiment:.4f}")
        return float(sentiment)
    
    def _analyze_basic(self, text: str) -> float:
        """Basic sentiment analysis using keyword matching."""
        logger.debug(f"Analyzing sentiment (basic) for text: {text[:50]}...")
        
        text_lower = text.lower()
        
        positive_words = [
            'good', 'great', 'excellent', 'happy', 'joy', 'love', 'wonderful',
            'fantastic', 'amazing', 'super', 'best', 'awesome', 'brilliant',
            'positive', 'pleasant', 'delightful', 'perfect', 'beautiful', 'better'
        ]
        
        negative_words = [
            'bad', 'terrible', 'awful', 'sad', 'hate', 'horrible', 'worst',
            'poor', 'negative', 'unpleasant', 'depressed', 'anxious', 'worried',
            'angry', 'frustrated', 'disappointed', 'miserable', 'unhappy', 'worse'
        ]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        
        # Normalize to [-1, 1]
        score = (positive_count - negative_count) / total
        logger.debug(f"Sentiment analysis result: {score:.4f}")
        return float(score)
    
    def is_loaded(self) -> bool:
        """Check if model is loaded and ready."""
        if self.mode == "transformers":
            return self.pipeline is not None
        elif self.mode in ["textblob", "basic"]:
            return True  # Fallback methods always work
        return False


# Global singleton instance
_sentiment_model: SentimentModel = None


def get_sentiment_model() -> SentimentModel:
    """Get or create the global sentiment model instance."""
    global _sentiment_model
    if _sentiment_model is None:
        _sentiment_model = SentimentModel()
    return _sentiment_model
