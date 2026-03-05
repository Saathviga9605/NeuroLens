"""
Fallback sentiment model for Python 3.13 compatibility.
Uses TextBlob as a simple alternative when transformers/torch are incompatible.
"""
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Try importing transformers, fall back to TextBlob if not available
TRANSFORMERS_AVAILABLE = False
TEXTBLOB_AVAILABLE = False

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
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


class FallbackSentimentModel:
    """Simple sentiment analyzer using TextBlob."""
    
    def __init__(self):
        self.loaded = TEXTBLOB_AVAILABLE
        logger.info(f"FallbackSentimentModel initialized (TextBlob available: {self.loaded})")
    
    def analyze(self, text: str) -> float:
        """
        Analyze sentiment of text.
        Returns: sentiment score in range [-1, 1]
        """
        if not text or not text.strip():
            return 0.0
        
        if TEXTBLOB_AVAILABLE:
            try:
                from textblob import TextBlob
                blob = TextBlob(text)
                # TextBlob polarity is already in [-1, 1]
                sentiment = blob.sentiment.polarity
                return float(sentiment)
            except Exception as e:
                logger.error(f"TextBlob analysis failed: {e}")
                return 0.0
        else:
            # Ultra-basic sentiment using keyword matching
            return self._basic_sentiment(text)
    
    def _basic_sentiment(self, text: str) -> float:
        """Very basic sentiment analysis based on keywords."""
        text_lower = text.lower()
        
        positive_words = [
            'good', 'great', 'excellent', 'happy', 'joy', 'love', 'wonderful',
            'fantastic', 'amazing', 'super', 'best', 'awesome', 'brilliant',
            'positive', 'pleasant', 'delightful', 'perfect', 'beautiful'
        ]
        
        negative_words = [
            'bad', 'terrible', 'awful', 'sad', 'hate', 'horrible', 'worst',
            'poor', 'negative', 'unpleasant', 'depressed', 'anxious', 'worried',
            'angry', 'frustrated', 'disappointed', 'miserable', 'unhappy'
        ]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        
        # Normalize to [-1, 1]
        score = (positive_count - negative_count) / total
        return float(score)
    
    def is_loaded(self) -> bool:
        """Check if model is ready."""
        return True  # Fallback always works


class TransformersSentimentModel:
    """Advanced sentiment model using Hugging Face transformers."""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Load sentiment analysis model."""
        try:
            # Use a lightweight sentiment model
            model_name = "distilbert-base-uncased-finetuned-sst-2-english"
            self.pipeline = pipeline("sentiment-analysis", model=model_name, device=-1)
            logger.info(f"Loaded sentiment model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load transformers model: {e}")
            self.pipeline = None
    
    def analyze(self, text: str) -> float:
        """
        Analyze sentiment using transformers.
        Returns: sentiment score in range [-1, 1]
        """
        if not self.pipeline:
            logger.warning("Transformers model not available, returning neutral")
            return 0.0
        
        if not text or not text.strip():
            return 0.0
        
        try:
            result = self.pipeline(text[:512])[0]  # Limit text length
            label = result['label']
            score = result['score']
            
            # Convert to [-1, 1] scale
            if label == 'POSITIVE':
                return float(score)
            else:  # NEGATIVE
                return float(-score)
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return 0.0
    
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.pipeline is not None


# Singleton instance
_sentiment_model: Optional[object] = None


def get_sentiment_model():
    """
    Get sentiment model instance (singleton).
    Automatically selects best available model.
    """
    global _sentiment_model
    
    if _sentiment_model is None:
        if TRANSFORMERS_AVAILABLE:
            try:
                _sentiment_model = TransformersSentimentModel()
                if _sentiment_model.is_loaded():
                    logger.info("Using Transformers sentiment model")
                else:
                    raise Exception("Transformers model failed to load")
            except Exception as e:
                logger.warning(f"Falling back to simple model: {e}")
                _sentiment_model = FallbackSentimentModel()
        else:
            logger.info("Using fallback sentiment model")
            _sentiment_model = FallbackSentimentModel()
    
    return _sentiment_model
