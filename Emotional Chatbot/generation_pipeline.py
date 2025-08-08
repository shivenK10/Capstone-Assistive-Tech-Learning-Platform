from causal_model_handler import ModelHandler
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict
from logger import Logger

logger = Logger(name="Enhanced Generation", log_file_needed=True, log_file='Logs/enhanced_generation.log', level='DEV')

class EducationalEmotionalResponseGenerator:
    def __init__(self, model_name="meta-llama/Llama-3.2-1B-Instruct"):
        logger.debug(f"Initializing EducationalEmotionalResponseGenerator with model: {model_name}")
        try:
            self.handler = ModelHandler(model_name, True)
            model, tokenizer = self.handler.load_model()
            
            self.gen_pipe = pipeline(
                task="text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=150,
                min_new_tokens=50,
                temperature=0.3,
                top_p=0.9,
                top_k=50,
                repetition_penalty=1.1,
                do_sample=True,
                return_full_text=False,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
            )
            
            self.llm_chain = HuggingFacePipeline(pipeline=self.gen_pipe)
            
            self.templates = {
                'dyslexia_supportive': """You are a patient, understanding AI tutor specializing in helping children with dyslexia. You understand reading challenges and provide supportive assistance.

Student's message: {user_input}
Detected emotion: {emotion_label}
Educational context: {educational_context}

Guidelines:
- Acknowledge their reading/writing challenges with empathy
- Offer alternative learning methods (audio, visual, kinesthetic)
- Use simple, clear language with shorter sentences
- Suggest tools like text-to-speech or special fonts
- Be patient and encouraging about progress
- Break complex information into smaller chunks

Response:""",

                'adhd_supportive': """You are an energetic, understanding AI tutor who helps children with ADHD stay focused and engaged in learning.

Student's message: {user_input}
Detected emotion: {emotion_label}
Educational context: {educational_context}

Guidelines:
- Acknowledge their attention challenges without judgment
- Suggest movement breaks or fidget strategies
- Keep responses concise and well-structured
- Use engaging, interactive language
- Offer multiple short activities instead of long tasks
- Celebrate small wins and progress
- Help them refocus when distracted

Response:""",

                'learning_supportive': """You are a compassionate AI tutor who helps children overcome learning difficulties with patience and creativity.

Student's message: {user_input}
Detected emotion: {emotion_label}
Educational context: {educational_context}

Guidelines:
- Validate their feelings about learning challenges
- Offer alternative explanations and approaches
- Use encouraging, growth-mindset language
- Suggest breaking tasks into smaller steps
- Provide specific, actionable help
- Remind them that everyone learns differently
- Celebrate effort over perfection

Response:""",

                'confidence_building': """You are an encouraging AI tutor focused on building student confidence and self-esteem.

Student's message: {user_input}
Detected emotion: {emotion_label}
Educational context: {educational_context}

Guidelines:
- Address negative self-talk with gentle correction
- Highlight their strengths and past successes
- Use growth mindset language ("yet", "learning", "growing")
- Provide specific, achievable next steps
- Share that mistakes are part of learning
- Be enthusiastic about their potential
- Ask about their interests to build connections

Response:""",

                'standard': """You are a friendly, supportive AI tutor who helps children with their learning in an encouraging way.

Student's message: {user_input}
Detected emotion: {emotion_label}

Guidelines:
- Be warm, patient, and age-appropriate
- Acknowledge their emotions with empathy
- Provide helpful, educational responses
- Encourage curiosity and questions
- Keep responses engaging and conversational
- Celebrate learning moments
- Ask follow-up questions when appropriate

Response:"""
            }
            
            logger.debug("Educational response generation pipeline loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load enhanced generation model: {str(e)}")
            raise

    def generate_educational_response(self, user_input: str, emotion_analysis: Dict) -> str:
        """
        Generate context-aware educational response
        """
        logger.debug(f"Generating educational response for emotion analysis: {emotion_analysis}")
        
        try:
            if not user_input or not user_input.strip():
                return "I'm here to help you learn! What would you like to talk about or work on today?"
            
            recommended_approach = emotion_analysis.get('recommended_approach', 'standard')
            template_key = recommended_approach if recommended_approach in self.templates else 'standard'
            
            logger.debug(f"Using template: {template_key}")
            
            template = self.templates[template_key]
            prompt = PromptTemplate.from_template(template)
            chain = prompt | self.llm_chain | StrOutputParser()
            
            inputs = {
                "user_input": user_input.strip(),
                "emotion_label": emotion_analysis.get('primary_emotion', 'neutral'),
            }
            
            if 'educational_context' in emotion_analysis:
                inputs["educational_context"] = emotion_analysis['educational_context']
            
            logger.debug("Invoking enhanced generation chain")
            result = chain.invoke(inputs)
            
            response = result.strip()
            
            prefixes_to_remove = ["Response:", "Assistant:", "AI:", "Bot:", "Tutor:"]
            for prefix in prefixes_to_remove:
                if response.startswith(prefix):
                    response = response[len(prefix):].strip()
            
            response = self._enhance_response_for_special_needs(
                response, emotion_analysis.get('special_needs_indicators', [])
            )
            
            if len(response) < 15:
                return self._get_educational_fallback(emotion_analysis)
            
            logger.debug(f"Generated educational response: {len(response)} characters")
            return response
            
        except Exception as e:
            logger.error(f"Error generating educational response: {str(e)}")
            return self._get_educational_fallback(emotion_analysis)
    
    def _enhance_response_for_special_needs(self, response: str, indicators: list) -> str:
        """Add special formatting or suggestions based on special needs indicators"""
        if 'dyslexia_pattern' in indicators:
            if len(response) > 100:
                response += "\n\n💡 Tip: Try using text-to-speech or a dyslexia-friendly font if reading this is challenging!"
        
        elif 'adhd_pattern' in indicators:
            response += "\n\n⚡ Remember: It's okay to take a movement break if you need one!"
        
        return response
    
    def _get_educational_fallback(self, emotion_analysis: Dict) -> str:
        """Educational fallback responses"""
        emotion = emotion_analysis.get('primary_emotion', 'neutral')
        context = emotion_analysis.get('educational_context', 'general')
        
        fallbacks = {
            ('sadness', 'frustration_learning'): "Learning can feel hard sometimes, and that's completely normal! Every student faces challenges. What specific part would you like help with? We can break it down together.",
            ('anger', 'frustration_learning'): "I can hear that you're really frustrated with this. That's okay - learning new things can be tough! Let's take a step back and try a different approach. What's the hardest part for you?",
            ('fear', 'anxiety_learning'): "It's natural to feel nervous about learning new things. You're brave for trying! Remember, making mistakes is how we learn. What would help you feel more confident?",
            ('neutral', 'dyslexia_pattern'): "I understand that reading and writing can be challenging. There are many ways to learn, and we'll find what works best for you. What would you like to work on?",
            ('neutral', 'adhd_pattern'): "I know it can be hard to focus sometimes. That's okay! Let's find ways to make learning more engaging and fun for you. What interests you most?",
        }
        
        key = (emotion, context)
        if key in fallbacks:
            return fallbacks[key]
        
        return "I'm here to help you learn and grow! Every question you have is important. What would you like to explore together?"

educational_response_generator = EducationalEmotionalResponseGenerator()

def generate_educational_response(user_input: str, emotion_analysis: Dict) -> str:
    """Global function for educational response generation"""
    return educational_response_generator.generate_educational_response(user_input, emotion_analysis)
