from sequence_model_handler import SequenceModelHandler
from transformers import pipeline
import re
from typing import Dict, Tuple, List
from logger import Logger
import warnings

warnings.filterwarnings("ignore")

logger = Logger(name="Enhanced Emotion Detection", log_file_needed=True, log_file='Logs/emotion_detection.log', level='DEV')

class EmotionDetector:
    def __init__(self, model_name="bhadresh-savani/bert-base-uncased-emotion"):
        logger.debug(f"Initializing EnhancedEmotionDetector with model: {model_name}")
        try:
            self.model_handler = SequenceModelHandler(model_name)
            loaded_model, corresponding_tokenizer = self.model_handler.load_sequence_model()
            
            self.emotion_classifier = pipeline(
                task="text-classification",
                model=loaded_model,
                tokenizer=corresponding_tokenizer,
                return_all_scores=True,
                top_k=6,
            )
            
            self.educational_patterns = {
                'frustration_learning': [
                    r"(?i)(can't|cannot|don't know|don't understand|too hard|difficult|confused|stuck)",
                    r"(?i)(hate|stupid|dumb|impossible|give up|quit)"
                ],
                'anxiety_learning': [
                    r"(?i)(worried|scared|nervous|afraid|anxious|test|exam|grade)",
                    r"(?i)(what if|don't want to|scared to try)"
                ],
                'confidence_low': [
                    r"(?i)(not good at|bad at|terrible at|can't do|not smart)",
                    r"(?i)(everyone else|better than me|not like others)"
                ],
                'engagement_positive': [
                    r"(?i)(love|like|fun|cool|awesome|amazing|interesting)",
                    r"(?i)(want to learn|excited|can't wait|show me)"
                ],
                'adhd_indicators': [
                    r"(?i)(bored|boring|restless|can't sit|need to move|distracted)",
                    r"(?i)(forgot|keep forgetting|lost focus|mind wandering)"
                ],
                'dyslexia_indicators': [
                    r"(?i)(words are|letters are|jumbled|mixed up|backwards|blurry)",
                    r"(?i)(hard to read|can't see|words moving|letters dancing)"
                ]
            }
            
            logger.debug("Enhanced emotion detection model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load enhanced emotion detection model: {str(e)}")
            raise

    def detect_educational_emotion(self, text: str, context: Dict = None) -> Dict:
        """
        Enhanced emotion detection with educational context awareness
        """
        logger.debug(f"Starting enhanced emotion detection for text: '{text[:50]}...'")
        
        if not text or not text.strip():
            logger.warning("Empty text provided")
            return {
                'primary_emotion': 'neutral',
                'confidence': 0.0,
                'educational_context': 'unknown',
                'special_needs_indicators': [],
                'recommended_approach': 'standard'
            }
        
        try:
            base_emotion, confidence = self._detect_base_emotion(text)
            
            educational_context = self._analyze_educational_context(text)
            
            special_needs = self._detect_special_needs_indicators(text)
            
            result = {
                'primary_emotion': base_emotion,
                'confidence': confidence,
                'educational_context': educational_context,
                'special_needs_indicators': special_needs,
                'recommended_approach': self._get_recommended_approach(
                    base_emotion, educational_context, special_needs
                ),
                'context_factors': context or {}
            }
            
            logger.debug(f"Enhanced emotion analysis complete: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in enhanced emotion detection: {str(e)}")
            return {
                'primary_emotion': 'neutral',
                'confidence': 0.0,
                'educational_context': 'error',
                'special_needs_indicators': [],
                'recommended_approach': 'supportive'
            }
    
    def _detect_base_emotion(self, text: str) -> Tuple[str, float]:
        """Your existing emotion detection logic"""
        preds = self.emotion_classifier(text)
        
        if isinstance(preds, list) and len(preds) > 0:
            batch = preds[0] if isinstance(preds[0], list) else preds
        else:
            batch = preds
            
        if isinstance(batch, list) and len(batch) > 0:
            best = batch[0]
            label = best["label"].lower()
            score = float(best["score"])
            
            if score < 0.6:
                return "neutral", score
                
            return label, score
        
        return "neutral", 0.0
    
    def _analyze_educational_context(self, text: str) -> str:
        """Analyze if the message is related to learning difficulties"""
        for context_type, patterns in self.educational_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    logger.debug(f"Educational context detected: {context_type}")
                    return context_type
        
        return 'general'
    
    def _detect_special_needs_indicators(self, text: str) -> List[str]:
        """Detect indicators of ADHD or dyslexia"""
        indicators = []
        
        for pattern in self.educational_patterns['adhd_indicators']:
            if re.search(pattern, text):
                indicators.append('adhd_pattern')
                break
        
        for pattern in self.educational_patterns['dyslexia_indicators']:
            if re.search(pattern, text):
                indicators.append('dyslexia_pattern')
                break
        
        return indicators
    
    def _get_recommended_approach(self, emotion: str, context: str, indicators: List[str]) -> str:
        """Recommend response approach based on analysis"""
        if 'dyslexia_pattern' in indicators:
            return 'dyslexia_supportive'
        elif 'adhd_pattern' in indicators:
            return 'adhd_supportive'
        elif context in ['frustration_learning', 'anxiety_learning']:
            return 'learning_supportive'
        elif context == 'confidence_low':
            return 'confidence_building'
        elif context == 'engagement_positive':
            return 'encouraging'
        else:
            return 'standard'

emotion_detector = EmotionDetector()

def detect_enhanced_emotion(text: str, context: Dict = None) -> Dict:
    """Global function for enhanced emotion detection"""
    return emotion_detector.detect_educational_emotion(text, context)
