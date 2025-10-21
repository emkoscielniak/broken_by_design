"""
Service interfaces for the AI Learning Coach.

Following:
- Interface Segregation Principle (ISP): Small, focused interfaces
- Dependency Inversion Principle (DIP): High-level modules depend on these abstractions
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.models import (
    PromptAnalysis,
    PromptScore,
    Lesson,
    UserProgress,
)


class IPromptEvaluator(ABC):
    """
    ISP: Focused interface for prompt evaluation.
    DIP: High-level modules depend on this abstraction.
    
    This interface defines the contract for evaluating prompts.
    Different implementations can use different evaluation strategies.
    """
    
    @abstractmethod
    def evaluate(self, prompt: str, context: Optional[str] = None) -> PromptAnalysis:
        """
        Analyze a prompt and return detailed analysis.
        
        Args:
            prompt: The prompt text to evaluate
            context: Optional context for the evaluation
            
        Returns:
            PromptAnalysis with score and feedback
        """
        pass


class IScoreStrategy(ABC):
    """
    ISP: Focused on scoring only.
    OCP: Can add new strategies without changing evaluator.
    
    This interface defines the contract for scoring strategies.
    Implementations can use rules, AI, or hybrid approaches.
    """
    
    @abstractmethod
    def calculate_score(
        self, 
        prompt: str, 
        context: Optional[str] = None
    ) -> PromptScore:
        """
        Calculate score for a prompt.
        
        Args:
            prompt: The prompt text to score
            context: Optional context for scoring
            
        Returns:
            PromptScore object with all scoring dimensions
        """
        pass


class ILessonProvider(ABC):
    """
    ISP: Focused on lesson retrieval.
    DIP: LearningCoach depends on this, not concrete implementation.
    
    This interface defines the contract for accessing lesson content.
    Implementations can load from files, databases, or APIs.
    """
    
    @abstractmethod
    def get_lesson(self, lesson_id: str) -> Lesson:
        """
        Get specific lesson by ID.
        
        Args:
            lesson_id: Unique lesson identifier
            
        Returns:
            Lesson object
            
        Raises:
            ValueError: If lesson not found
        """
        pass
    
    @abstractmethod
    def get_lessons_by_level(self, level: int) -> List[Lesson]:
        """
        Get all lessons for a skill level.
        
        Args:
            level: Skill level (1-5)
            
        Returns:
            List of Lesson objects
        """
        pass
    
    @abstractmethod
    def get_next_lesson(self, current_lesson_id: str) -> Optional[Lesson]:
        """
        Get next lesson in sequence.
        
        Args:
            current_lesson_id: Current lesson ID
            
        Returns:
            Next Lesson object or None if no more lessons
        """
        pass


class IFeedbackProvider(ABC):
    """
    ISP: Focused on feedback generation.
    OCP: Can add new feedback styles.
    
    This interface defines the contract for generating user feedback.
    Implementations can provide different styles (detailed, concise, beginner).
    """
    
    @abstractmethod
    def generate_feedback(self, analysis: PromptAnalysis) -> str:
        """
        Generate human-readable feedback.
        
        Args:
            analysis: PromptAnalysis with score and details
            
        Returns:
            Formatted feedback string
        """
        pass


class IProgressPersister(ABC):
    """
    ISP: Focused on persistence only.
    DIP: Allows swapping storage backends.
    
    This interface defines the contract for persisting user progress.
    Implementations can use JSON files, databases, or cloud storage.
    """
    
    @abstractmethod
    def save(self, progress: UserProgress) -> None:
        """
        Save user progress.
        
        Args:
            progress: UserProgress object to save
            
        Raises:
            IOError: If save fails
        """
        pass
    
    @abstractmethod
    def load(self, user_id: str) -> UserProgress:
        """
        Load user progress.
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            UserProgress object (creates new if user doesn't exist)
        """
        pass


class IAIClient(ABC):
    """
    ISP: Minimal AI interaction interface.
    DIP: Allows mocking for tests, swapping providers.
    
    This interface defines the contract for AI communication.
    Implementations can use OpenAI, Claude, or other providers.
    """
    
    @abstractmethod
    def chat(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> str:
        """
        Send chat messages and get response.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            **kwargs: Additional parameters (model, temperature, etc.)
            
        Returns:
            AI response text
            
        Raises:
            Exception: If API call fails
        """
        pass
    
    @abstractmethod
    def analyze_prompt_intent(self, prompt: str) -> Dict[str, Any]:
        """
        Use AI to analyze prompt intent.
        
        Args:
            prompt: The prompt to analyze
            
        Returns:
            Dictionary with analysis results including:
                - total_score: float
                - learning_orientation: float
                - specificity: float
                - engagement: float
                - intent: str
                - reasoning: str
                
        Raises:
            Exception: If API call fails
        """
        pass
