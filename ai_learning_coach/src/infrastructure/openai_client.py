"""
OpenAI client implementation.

Provides AI-powered prompt analysis and chat functionality.

Demonstrates:
- DIP: Implements IAIClient interface
- SRP: Single responsibility of AI communication
"""

from typing import Optional
from openai import OpenAI
from src.interfaces import IAIClient
from src.models import PromptIntent


class OpenAIClient(IAIClient):
    """
    OpenAI API client for AI-powered features.
    
    Handles communication with OpenAI's API for chat and analysis.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key
            model: Model to use (default: gpt-4o-mini for cost efficiency)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Send a chat message and get AI response.
        
        Args:
            message: User message
            system_prompt: Optional system prompt to guide AI behavior
            
        Returns:
            AI response text
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content or ""
        
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
    
    def analyze_prompt_intent(self, prompt: str) -> PromptIntent:
        """
        Use AI to classify prompt intent.
        
        Args:
            prompt: The prompt to analyze
            
        Returns:
            Classified intent
        """
        system_prompt = """You are an expert at analyzing student prompts. 
        Classify the intent of the following prompt into one of these categories:
        - do_it_for_me: Student asking AI to complete their work
        - help_me_learn: Student asking for learning guidance
        - clarifying: Student asking for clarification
        - reflection: Student asking reflective questions
        - unknown: Cannot determine intent
        
        Respond with ONLY the category name, nothing else."""
        
        try:
            response = self.chat(prompt, system_prompt)
            intent_str = response.strip().lower()
            
            # Map response to PromptIntent enum
            intent_map = {
                "do_it_for_me": PromptIntent.DO_IT_FOR_ME,
                "help_me_learn": PromptIntent.HELP_ME_LEARN,
                "clarifying": PromptIntent.CLARIFYING,
                "reflection": PromptIntent.REFLECTION,
                "unknown": PromptIntent.UNKNOWN
            }
            
            return intent_map.get(intent_str, PromptIntent.UNKNOWN)
        
        except Exception:
            # Fallback to UNKNOWN if API fails
            return PromptIntent.UNKNOWN
