"""
PromptAnalyzer service implementation.

This service evaluates prompts using a scoring strategy and provides
detailed analysis including anti-patterns, strengths, and improvements.

Demonstrates:
- SRP: Single responsibility of analyzing prompts
- OCP: Open for extension via IScoreStrategy
- LSP: Works with any IScoreStrategy implementation
- DIP: Depends on IScoreStrategy abstraction, not concrete implementation
"""

from typing import List
from src.interfaces import IPromptEvaluator, IScoreStrategy
from src.models import PromptAnalysis, PromptScore, PromptIntent


class PromptAnalyzer(IPromptEvaluator):
    """
    Analyzes prompts for quality and learning effectiveness.
    
    Uses dependency injection to accept any IScoreStrategy implementation,
    demonstrating the Dependency Inversion Principle.
    """
    
    # Anti-pattern keywords to detect
    ANTI_PATTERN_KEYWORDS = {
        "do_it_for_me": [
            "write my", "do my", "complete my", "solve for me",
            "give me the answer", "just tell me", "do it for me"
        ],
        "complete_solution": [
            "complete solution", "entire code", "full implementation",
            "all the code", "whole program"
        ],
        "vague": [
            "stuff", "things", "help", "something", "anything"
        ],
        "passive": [
            "i don't understand", "i'm confused", "i can't"
        ]
    }
    
    # Strength keywords to identify
    STRENGTH_KEYWORDS = {
        "learning_oriented": [
            "explain", "teach me", "help me understand", "show me how",
            "walk me through", "demonstrate"
        ],
        "specific": [
            "specifically", "in particular", "focusing on", "regarding",
            "about", "concerning"
        ],
        "interactive": [
            "quiz me", "test my", "check my understanding", "give me practice",
            "challenge me", "then"
        ],
        "reflective": [
            "why", "how does", "what if", "difference between", "compare"
        ]
    }
    
    def __init__(self, scorer: IScoreStrategy):
        """
        Initialize analyzer with a scoring strategy.
        
        Args:
            scorer: Implementation of IScoreStrategy to use for scoring
        """
        self.scorer = scorer
    
    def evaluate(self, prompt: str) -> PromptAnalysis:
        """
        Evaluate a prompt and return detailed analysis.
        
        Args:
            prompt: The user's prompt to analyze
            
        Returns:
            PromptAnalysis with score, detected_patterns, strengths, and improvements
        """
        # Get score from strategy
        score = self.scorer.calculate_score(prompt)
        
        # Detect anti-patterns
        detected_patterns = self._detect_anti_patterns(prompt, score)
        
        # Identify strengths
        strengths = self._identify_strengths(prompt, score)
        
        # Generate improvements
        improvements = self._generate_improvements(prompt, score)
        
        # Generate example prompts
        examples = self._generate_examples(prompt, score)
        
        return PromptAnalysis(
            prompt=prompt,
            score=score,
            strengths=strengths,
            improvements=improvements,
            examples=examples,
            detected_patterns=detected_patterns
        )
    
    def _detect_anti_patterns(self, prompt: str, score: PromptScore) -> List[str]:
        """
        Detect anti-patterns in the prompt.
        
        Args:
            prompt: The prompt to analyze
            score: The calculated score
            
        Returns:
            List of detected anti-pattern descriptions
        """
        patterns = []
        prompt_lower = prompt.lower()
        
        # Empty or very short prompt
        if len(prompt.strip()) == 0:
            patterns.append("Empty prompt - no question or request provided")
        elif len(prompt.strip()) < 10:
            patterns.append("Very short prompt - lacks sufficient detail")
        
        # Check for "do it for me" intent
        if score.intent == PromptIntent.DO_IT_FOR_ME:
            patterns.append("Do-it-for-me pattern detected - asking AI to complete work instead of learning")
        
        # Check for complete solution requests
        for keyword in self.ANTI_PATTERN_KEYWORDS["complete_solution"]:
            if keyword in prompt_lower:
                patterns.append(f"Requesting complete solution - hinders learning by skipping problem-solving")
                break
        
        # Check for vague language
        vague_count = sum(1 for keyword in self.ANTI_PATTERN_KEYWORDS["vague"] 
                         if keyword in prompt_lower.split())
        if vague_count > 0 and score.specificity < 50:
            patterns.append("Vague language used - be more specific about what you want to learn")
        
        # Check for passive language
        passive_count = sum(1 for keyword in self.ANTI_PATTERN_KEYWORDS["passive"] 
                           if keyword in prompt_lower)
        if passive_count > 0:
            patterns.append("Passive framing - try asking 'explain' or 'teach me' instead of 'I don't understand'")
        
        return patterns
    
    def _identify_strengths(self, prompt: str, score: PromptScore) -> List[str]:
        """
        Identify strengths in the prompt.
        
        Args:
            prompt: The prompt to analyze
            score: The calculated score
            
        Returns:
            List of identified strength descriptions
        """
        strengths = []
        prompt_lower = prompt.lower()
        
        # Learning orientation
        if score.learning_orientation >= 60:
            learning_keywords_found = [kw for kw in self.STRENGTH_KEYWORDS["learning_oriented"] 
                                      if kw in prompt_lower]
            if learning_keywords_found:
                strengths.append(f"Learning-oriented approach using '{learning_keywords_found[0]}'")
        
        # Specificity
        if score.specificity >= 60:
            specific_keywords_found = [kw for kw in self.STRENGTH_KEYWORDS["specific"] 
                                      if kw in prompt_lower]
            if specific_keywords_found:
                strengths.append(f"Specific and focused on particular topics")
            elif len(prompt) >= 50:
                strengths.append("Good level of detail provided")
        
        # Interactive elements
        if score.engagement >= 60:
            interactive_keywords_found = [kw for kw in self.STRENGTH_KEYWORDS["interactive"] 
                                         if kw in prompt_lower]
            if interactive_keywords_found:
                strengths.append(f"Interactive learning requested ('{interactive_keywords_found[0]}')")
        
        # Reflective thinking
        reflective_keywords_found = [kw for kw in self.STRENGTH_KEYWORDS["reflective"] 
                                    if kw in prompt_lower]
        if reflective_keywords_found:
            strengths.append(f"Demonstrates reflective thinking with '{reflective_keywords_found[0]}'")
        
        # Multi-step approach
        if "then" in prompt_lower or "," in prompt:
            strengths.append("Multi-step learning approach")
        
        return strengths
    
    def _generate_improvements(self, prompt: str, score: PromptScore) -> List[str]:
        """
        Generate improvement suggestions based on score.
        
        Args:
            prompt: The prompt to analyze
            score: The calculated score
            
        Returns:
            List of improvement suggestions
        """
        improvements = []
        
        # Only suggest improvements if score is below passing
        if score.total_score >= 70:
            return improvements
        
        # Find the weakest dimension
        dimensions = {
            "learning_orientation": score.learning_orientation,
            "specificity": score.specificity,
            "engagement": score.engagement
        }
        
        weakest = min(dimensions, key=dimensions.get)
        weakest_score = dimensions[weakest]
        
        # Generate targeted improvements
        if weakest == "learning_orientation" and weakest_score < 60:
            improvements.append(
                "Rephrase to focus on learning: Use 'explain', 'teach me', or 'help me understand' "
                "instead of 'write', 'do', or 'give me'"
            )
        
        if weakest == "specificity" and weakest_score < 60:
            improvements.append(
                "Add more specific details: Include what topic, what aspect, or what context you're interested in"
            )
            if len(prompt.strip()) < 20:
                improvements.append(
                    "Expand your prompt: Provide more context and detail about what you want to learn"
                )
        
        if weakest == "engagement" and weakest_score < 60:
            improvements.append(
                "Request interactive learning: Ask for quizzes, examples, or practice problems"
            )
            improvements.append(
                "Use multi-step prompts: For example, 'Explain X, then quiz me, then give me practice problems'"
            )
        
        # If intent is wrong, provide specific guidance
        if score.intent == PromptIntent.DO_IT_FOR_ME:
            improvements.append(
                "Shift from 'do it for me' to 'teach me how': Instead of asking AI to complete your work, "
                "ask it to guide you through the process"
            )
        
        # If all dimensions are low, provide general guidance
        if all(score < 50 for score in dimensions.values()):
            improvements.append(
                "Example of a strong prompt: 'Explain how Python decorators work, provide examples, "
                "then quiz me to check my understanding'"
            )
        
        return improvements
    
    def _generate_examples(self, prompt: str, score: PromptScore) -> List[str]:
        """
        Generate example better prompts based on weaknesses.
        
        Args:
            prompt: The original prompt
            score: The calculated score
            
        Returns:
            List of example improved prompts
        """
        examples = []
        
        # Only generate examples if score is below passing
        if score.total_score >= 70:
            return examples
        
        # Generate examples based on intent and weaknesses
        if score.intent == PromptIntent.DO_IT_FOR_ME:
            examples.append(
                "Instead of 'Write my essay about climate change', try: "
                "'Explain the key arguments about climate change, then help me organize my thoughts'"
            )
            examples.append(
                "Instead of 'Do my homework', try: "
                "'Teach me the concepts I need, then quiz me to verify my understanding'"
            )
        
        if score.specificity < 50:
            examples.append(
                "Instead of 'Help me with Python', try: "
                "'Explain how Python list comprehensions work with examples'"
            )
            examples.append(
                "Instead of 'Explain stuff', try: "
                "'Explain the difference between stacks and queues, focusing on use cases'"
            )
        
        if score.engagement < 50:
            examples.append(
                "Try adding: '...then quiz me to test my understanding'"
            )
            examples.append(
                "Try adding: '...provide practice problems I can work through'"
            )
        
        # Provide general strong example if no specific examples added
        if not examples:
            examples.append(
                "'Explain how recursion works in Python, provide examples with base cases, "
                "then give me practice problems to solve'"
            )
        
        return examples
