"""
Data models for the AI Learning Coach application.

This module defines the core data structures used throughout the application,
following the Single Responsibility Principle (SRP).
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class PromptIntent(Enum):
    """
    Types of prompt intents.
    
    Categorizes user prompts based on their learning orientation.
    """
    DO_IT_FOR_ME = "do_it_for_me"      # Bad: "Write my essay"
    HELP_ME_LEARN = "help_me_learn"    # Good: "Explain and quiz me"
    CLARIFYING = "clarifying"          # Good: "What do you mean by X?"
    REFLECTION = "reflection"          # Good: "How does this relate to Y?"
    UNKNOWN = "unknown"


@dataclass
class PromptScore:
    """
    SRP: Only represents score data.
    Immutable value object for prompt evaluation scores.
    
    Attributes:
        total_score: Overall score 0-100
        learning_orientation: How learning-focused the prompt is (0-100)
        specificity: How clear and specific the prompt is (0-100)
        engagement: How much it encourages interaction (0-100)
        intent: The classified intent of the prompt
    """
    total_score: float
    learning_orientation: float
    specificity: float
    engagement: float
    intent: PromptIntent
    
    def __post_init__(self):
        """Validate score ranges."""
        for score_name in ['total_score', 'learning_orientation', 'specificity', 'engagement']:
            score = getattr(self, score_name)
            if not 0 <= score <= 100:
                raise ValueError(f"{score_name} must be between 0 and 100, got {score}")
    
    @property
    def is_passing(self) -> bool:
        """Minimum 60% to pass."""
        return self.total_score >= 60.0


@dataclass
class PromptAnalysis:
    """
    SRP: Complete analysis results.
    Contains score + detailed feedback.
    
    Attributes:
        prompt: The original prompt text
        score: The calculated score
        strengths: List of what the user did well
        improvements: List of suggestions for improvement
        examples: List of better alternative prompts
        detected_patterns: List of anti-patterns found
    """
    prompt: str
    score: PromptScore
    strengths: List[str]
    improvements: List[str]
    examples: List[str]
    detected_patterns: List[str]


@dataclass
class Exercise:
    """
    Practice exercise within a lesson.
    
    Attributes:
        id: Unique exercise identifier
        prompt: The exercise prompt/question
        expected_intent: The intent students should demonstrate
        hints: List of hints to help students
        good_example: Example of a good response
        bad_example: Example of a bad response
    """
    id: str
    prompt: str
    expected_intent: PromptIntent
    hints: List[str]
    good_example: str
    bad_example: str


@dataclass
class Lesson:
    """
    SRP: Lesson content only.
    OCP: Can extend with new lesson types.
    
    Attributes:
        id: Unique lesson identifier
        title: Lesson title
        description: Brief description
        learning_objectives: List of what students will learn
        difficulty: Difficulty level 1-5
        content: Main lesson content/text
        exercises: Practice exercises for this lesson
    """
    id: str
    title: str
    description: str
    learning_objectives: List[str]
    difficulty: int
    content: str
    exercises: List[Exercise] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate difficulty level."""
        if not 1 <= self.difficulty <= 5:
            raise ValueError(f"Difficulty must be between 1 and 5, got {self.difficulty}")


@dataclass
class UserProgress:
    """
    SRP: User state tracking only.
    
    Attributes:
        user_id: Unique user identifier
        current_lesson: Current lesson number
        completed_lessons: List of completed lesson IDs
        prompt_history: History of analyzed prompts
        skill_level: User's skill level 1-5
        total_prompts: Total number of prompts submitted
        good_prompts: Number of prompts with score >= 60
    """
    user_id: str
    current_lesson: int
    completed_lessons: List[str]
    prompt_history: List[PromptAnalysis]
    skill_level: int
    total_prompts: int
    good_prompts: int
    
    def __post_init__(self):
        """Validate skill level."""
        if not 1 <= self.skill_level <= 5:
            raise ValueError(f"Skill level must be between 1 and 5, got {self.skill_level}")
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_prompts == 0:
            return 0.0
        return (self.good_prompts / self.total_prompts) * 100


@dataclass
class CoachConfig:
    """
    SRP: Configuration data only.
    Immutable settings for the learning coach.
    
    Attributes:
        api_key: OpenAI API key
        model: OpenAI model to use
        feedback_style: Style of feedback (detailed, concise, beginner)
        auto_advance: Whether to auto-advance to next lesson
        save_history: Whether to save prompt history
    """
    api_key: str
    model: str = "gpt-4o-mini"
    feedback_style: str = "detailed"
    auto_advance: bool = False
    save_history: bool = True
    
    def __post_init__(self):
        """Validate configuration."""
        if not self.api_key:
            raise ValueError("API key cannot be empty")
        
        valid_styles = ["detailed", "concise", "beginner"]
        if self.feedback_style not in valid_styles:
            raise ValueError(f"feedback_style must be one of {valid_styles}")


@dataclass
class ScoreWeights:
    """
    SRP: Scoring configuration.
    OCP: Can add new weights without changing scoring logic.
    
    Attributes:
        learning_orientation: Weight for learning orientation (0-1)
        specificity: Weight for specificity (0-1)
        engagement: Weight for engagement (0-1)
    """
    learning_orientation: float = 0.4
    specificity: float = 0.3
    engagement: float = 0.3
    
    def __post_init__(self):
        """Validate weights sum to 1.0."""
        total = self.learning_orientation + self.specificity + self.engagement
        if not 0.99 <= total <= 1.01:  # Allow for floating point precision
            raise ValueError(f"Weights must sum to 1.0, got {total}")


@dataclass
class DemonstrationResult:
    """
    SRP: Holds demonstration comparison data.
    
    Shows the difference between a bad prompt response and an improved version.
    Used to demonstrate the real impact of prompt quality.
    
    Attributes:
        original_prompt: The user's original (possibly bad) prompt
        improved_prompt: The improved version of the prompt
        bad_response: AI response to the original prompt (intentionally unhelpful)
        good_response: AI response to the improved prompt (helpful and educational)
        explanation: Why the improved version works better
        is_simulated: True if using canned examples instead of real API calls
    """
    original_prompt: str
    improved_prompt: str
    bad_response: str
    good_response: str
    explanation: str
    is_simulated: bool = False
