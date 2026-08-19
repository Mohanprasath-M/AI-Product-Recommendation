import re
import logging
from typing import Dict, Any, List, Tuple
from app.ml.model_registry import registry

logger = logging.getLogger(__name__)


class ReviewSentimentAnalyzer:
    """Local NLP review sentiment analyzer and topic extractor without external APIs."""

    def __init__(self):
        self._load_model()
        self.positive_keywords = {
            "great", "excellent", "perfect", "good", "amazing", "love", "best", "fast",
            "battery", "comfortable", "quality", "durable", "easy", "clear", "sound",
            "stylish", "value", "awesome", "smooth", "reliable", "bright", "sturdy",
            "sleek", "worth", "satisfied", "superb", "impressive", "recommend"
        }
        self.negative_keywords = {
            "bad", "terrible", "poor", "broken", "slow", "worst", "hate", "noisy",
            "cheap", "difficult", "heavy", "defective", "disappointed", "failed", "bug",
            "delay", "lag", "charging", "battery", "microphone", "uncomfortable", "scratch",
            "stopped", "issue", "problem", "waste", "return", "refund"
        }

    def _load_model(self):
        self.artifact = registry.load_artifact("sentiment_model")
        # artifact contains: {'vectorizer': tfidf, 'model': log_reg, 'labels': ['NEGATIVE', 'NEUTRAL', 'POSITIVE']}

    def reload(self):
        self._load_model()

    def analyze_text(self, text: str) -> Dict[str, Any]:
        if not text:
            return {
                "sentiment_label": "NEUTRAL",
                "sentiment_score": 0.0,
                "positive_topics": [],
                "negative_topics": []
            }

        cleaned = re.sub(r"[^\w\s]", " ", text.lower())
        words = set(cleaned.split())

        pos_topics = list(words.intersection(self.positive_keywords))[:5]
        neg_topics = list(words.intersection(self.negative_keywords))[:5]

        # ML Model prediction if loaded
        if self.artifact and "vectorizer" in self.artifact and "model" in self.artifact:
            vec = self.artifact["vectorizer"].transform([text])
            model = self.artifact["model"]
            pred = model.predict(vec)[0]
            probs = model.predict_proba(vec)[0]
            # Probabilities: [prob_neg, prob_neu, prob_pos]
            score = float(probs[-1] - probs[0])  # scale between -1.0 and 1.0
            label = str(pred)
        else:
            # Rule-based fallback if ML model is training/untrained
            pos_count = len(pos_topics)
            neg_count = len(neg_topics)
            if pos_count > neg_count:
                label = "POSITIVE"
                score = 0.75
            elif neg_count > pos_count:
                label = "NEGATIVE"
                score = -0.75
            else:
                label = "NEUTRAL"
                score = 0.0

        return {
            "sentiment_label": label,
            "sentiment_score": round(score, 3),
            "positive_topics": pos_topics,
            "negative_topics": neg_topics
        }


sentiment_analyzer = ReviewSentimentAnalyzer()
