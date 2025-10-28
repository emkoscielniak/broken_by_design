"""
Score strategies for prompt evaluation.

Following:
- Single Responsibility Principle (SRP): Each scorer has one job
- Open/Closed Principle (OCP): Can add new strategies without modifying existing
- Liskov Substitution Principle (LSP): All strategies are interchangeable
"""

from typing import Optional
from src.interfaces import IScoreStrategy
from src.models import PromptScore, PromptIntent, ScoreWeights


class RubricScorer(IScoreStrategy):
    """
    LSP: Can substitute for IScoreStrategy.
    OCP: Scoring logic isolated, can be extended.
    
    Uses rule-based rubric to score prompts.
    Fast, predictable, no API calls needed.
    """
    
    def __init__(self, weights: Optional[ScoreWeights] = None):
        """
        Initialize rubric scorer.
        
        Args:
            weights: Optional custom weights for scoring dimensions
        """
        self.weights = weights or ScoreWeights()
    
    def calculate_score(
        self, 
        prompt: str, 
        context: Optional[str] = None
    ) -> PromptScore:
        """
        Calculate score using rubric.
        
        Args:
            prompt: The prompt text to score
            context: Optional context (not used in rubric scoring)
            
        Returns:
            PromptScore with all dimensions
        """
        learning = self._score_learning_orientation(prompt)
        specificity = self._score_specificity(prompt)
        engagement = self._score_engagement(prompt)
        intent = self._classify_intent(prompt)
        
        total = (
            learning * self.weights.learning_orientation +
            specificity * self.weights.specificity +
            engagement * self.weights.engagement
        )
        
        return PromptScore(
            total_score=round(total, 1),
            learning_orientation=round(learning, 1),
            specificity=round(specificity, 1),
            engagement=round(engagement, 1),
            intent=intent
        )
    
    def _score_learning_orientation(self, prompt: str) -> float:
        """
        Score how learning-focused the prompt is.
        
        Args:
            prompt: The prompt text
            
        Returns:
            Score from 0-100
        """
        score = 50.0  # Base score
        prompt_lower = prompt.lower()
        
        # Learning keywords (add points)
        learning_keywords = [
            "explain", "teach", "help me understand", 
            "why", "how does", "can you show me",
            "walk me through", "break down", "clarify",
            "guide me", "help me learn"
        ]
        
        # Anti-learning keywords (subtract points)
        anti_keywords = [
            "write my", "do my", "give me the answer",
            "solve this for me", "just tell me", "complete this"
        ]
        
        # Check for learning keywords
        for keyword in learning_keywords:
            if keyword in prompt_lower:
                score += 10
        
        # Check for anti-learning keywords
        for keyword in anti_keywords:
            if keyword in prompt_lower:
                score -= 20
        
        # Bonus for questions (indicates curiosity)
        if "?" in prompt:
            score += 5
        
        return max(0, min(100, score))
    
    def _score_specificity(self, prompt: str) -> float:
        """
        Score how specific and clear the prompt is.
        
        Args:
            prompt: The prompt text
            
        Returns:
            Score from 0-100
        """
        score = 50.0
        prompt_lower = prompt.lower()
        
        # Length indicates detail (but not too long)
        length = len(prompt)
        if 50 < length < 200:
            score += 15
        elif 200 <= length < 300:
            score += 10
        elif length < 20:
            score -= 15
        
        # Questions are often specific
        question_count = prompt.count("?")
        if question_count > 0:
            score += min(10, question_count * 5)
        
        # Context words indicate specificity
        context_words = [
            "because", "specifically", "in the context of",
            "for example", "such as", "regarding"
        ]
        for word in context_words:
            if word in prompt_lower:
                score += 8
        
        # Vague words reduce specificity
        vague_words = ["something", "anything", "stuff", "things"]
        for word in vague_words:
            if word in prompt_lower:
                score -= 10
        
        return max(0, min(100, score))
    
    def _score_engagement(self, prompt: str) -> float:
        """
        Score how much the prompt encourages interaction.
        
        Args:
            prompt: The prompt text
            
        Returns:
            Score from 0-100
        """
        score = 50.0
        prompt_lower = prompt.lower()
        
        # Interactive keywords
        engagement_keywords = [
            "quiz me", "test my understanding", "ask me questions",
            "practice", "exercise", "check if", "verify",
            "challenge me", "give me problems", "let me try"
        ]
        
        for keyword in engagement_keywords:
            if keyword in prompt_lower:
                score += 15
        
        # Passive keywords (reduce engagement)
        passive_keywords = [
            "just tell me", "just give me", "simply explain"
        ]
        
        for keyword in passive_keywords:
            if keyword in prompt_lower:
                score -= 10
        
        # Multiple steps indicate engagement
        step_indicators = ["then", "after that", "next", "finally"]
        step_count = sum(1 for word in step_indicators if word in prompt_lower)
        if step_count > 0:
            score += min(15, step_count * 5)
        
        return max(0, min(100, score))
    
    def _classify_intent(self, prompt: str) -> PromptIntent:
        """
        Classify the prompt's intent.
        
        Args:
            prompt: The prompt text
            
        Returns:
            PromptIntent enum value
        """
        prompt_lower = prompt.lower()
        
        # Check for "do it for me" intent
        do_it_patterns = [
            "write my", "do my", "solve this for me",
            "complete this", "finish this", "create my"
        ]
        if any(pattern in prompt_lower for pattern in do_it_patterns):
            return PromptIntent.DO_IT_FOR_ME
        
        # Check for learning intent
        learning_patterns = [
            "explain", "teach me", "help me understand",
            "show me how", "walk me through", "quiz me"
        ]
        if any(pattern in prompt_lower for pattern in learning_patterns):
            return PromptIntent.HELP_ME_LEARN
        
        # Check for clarifying intent
        clarifying_patterns = [
            "what do you mean", "can you clarify", "i don't understand",
            "could you explain", "what does", "what is the difference"
        ]
        if any(pattern in prompt_lower for pattern in clarifying_patterns):
            return PromptIntent.CLARIFYING
        
        # Check for reflection intent
        reflection_patterns = [
            "how does this relate", "why is this", "what if",
            "how would this apply", "connect this to"
        ]
        if any(pattern in prompt_lower for pattern in reflection_patterns):
            return PromptIntent.REFLECTION
        
        return PromptIntent.UNKNOWN
