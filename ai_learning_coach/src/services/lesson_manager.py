"""
LessonManager service implementation.

This service manages lessons and provides lesson recommendations
based on user progress and skill level.

Demonstrates:
- SRP: Single responsibility of managing lessons
- OCP: Can be extended with new lesson selection strategies
- LSP: Implements ILessonProvider interface
- DIP: Returns abstractions (Lesson models) not implementation details
"""

from typing import List, Optional, Dict
from src.interfaces import ILessonProvider
from src.models import Lesson, UserProgress


class LessonManager(ILessonProvider):
    """
    Manages lessons and recommends appropriate lessons based on progress.
    
    Stores lessons in memory and provides filtering and recommendation logic.
    """
    
    def __init__(self):
        """Initialize lesson manager with empty lesson catalog."""
        self._lessons: Dict[str, Lesson] = {}
    
    def get_lesson(self, lesson_id: str) -> Optional[Lesson]:
        """
        Get a specific lesson by ID.
        
        Args:
            lesson_id: The ID of the lesson to retrieve
            
        Returns:
            The lesson if found, None otherwise
        """
        return self._lessons.get(lesson_id)
    
    def get_lessons_by_level(self, difficulty: int) -> List[Lesson]:
        """
        Get all lessons at a specific difficulty level.
        
        Args:
            difficulty: The difficulty level (1-5)
            
        Returns:
            List of lessons at the specified difficulty
        """
        return [
            lesson for lesson in self._lessons.values()
            if lesson.difficulty == difficulty
        ]
    
    def get_next_lesson(self, progress: UserProgress) -> Optional[Lesson]:
        """
        Recommend the next lesson based on user progress.
        
        Args:
            progress: The user's current progress
            
        Returns:
            The recommended next lesson, or None if no lessons available
        """
        # Determine appropriate difficulty level based on skill level (1-5)
        target_difficulty = progress.skill_level
        
        # Get lessons at appropriate difficulty
        candidate_lessons = self.get_lessons_by_level(target_difficulty)
        
        # Filter out completed lessons
        available_lessons = [
            lesson for lesson in candidate_lessons
            if lesson.id not in progress.completed_lessons
        ]
        
        # Return first available lesson, or None if all completed
        if available_lessons:
            return available_lessons[0]
        
        # If all lessons at current level completed, try next level
        if target_difficulty < 5:
            next_level_lessons = self.get_lessons_by_level(target_difficulty + 1)
            next_available = [
                lesson for lesson in next_level_lessons
                if lesson.id not in progress.completed_lessons
            ]
            if next_available:
                return next_available[0]
        
        return None
    
    def add_lesson(self, lesson: Lesson) -> None:
        """
        Add or update a lesson in the catalog.
        
        Args:
            lesson: The lesson to add
        """
        self._lessons[lesson.id] = lesson
    
    def get_all_lessons(self) -> List[Lesson]:
        """
        Get all lessons in the catalog.
        
        Returns:
            List of all lessons
        """
        return list(self._lessons.values())
    
    def load_default_lessons(self) -> None:
        """
        Load default lesson catalog.
        
        Provides sample lessons for testing and demonstration.
        """
        from src.models import Exercise, PromptIntent
        
        # Lesson 1: Prompting Basics
        lesson1 = Lesson(
            id="basics_001",
            title="Prompting Basics: Learning vs. Doing",
            description="Learn the difference between asking AI to do your work vs. asking it to help you learn.",
            learning_objectives=[
                "Identify 'do it for me' prompts",
                "Rephrase prompts to focus on learning",
                "Understand the value of learning-oriented requests"
            ],
            difficulty=1,
            content="Effective AI learning starts with how you ask questions. Instead of asking AI to complete your work, ask it to guide you through learning.",
            exercises=[
                Exercise(
                    id="basics_001_ex1",
                    prompt="Rephrase 'Write my code' to focus on learning",
                    expected_intent=PromptIntent.HELP_ME_LEARN,
                    hints=["Use words like 'explain', 'teach', or 'help me understand'"],
                    good_example="Explain how to write this code, then guide me through implementing it myself",
                    bad_example="Write my code for me"
                )
            ]
        )
        
        # Lesson 2: Being Specific
        lesson2 = Lesson(
            id="specificity_001",
            title="The Power of Specificity",
            description="Learn how to make your prompts clear and focused for better learning outcomes.",
            learning_objectives=[
                "Avoid vague language",
                "Provide context in questions",
                "Focus on specific topics"
            ],
            difficulty=1,
            content="Specific prompts lead to specific, useful answers. Include context and focus your questions.",
            exercises=[
                Exercise(
                    id="specificity_001_ex1",
                    prompt="Make this vague: 'Help with Python' into a specific learning question",
                    expected_intent=PromptIntent.HELP_ME_LEARN,
                    hints=["What specific Python topic?", "What aspect confuses you?"],
                    good_example="Explain how Python list comprehensions work, with examples of filtering and mapping",
                    bad_example="Help with Python"
                )
            ]
        )
        
        # Lesson 3: Interactive Learning  
        lesson3 = Lesson(
            id="interactive_001",
            title="Interactive Learning Strategies",
            description="Master the art of requesting quizzes, examples, and practice problems.",
            learning_objectives=[
                "Request interactive elements",
                "Create multi-step learning prompts",
                "Use examples and practice"
            ],
            difficulty=2,
            content="Interactive learning deepens understanding. Request quizzes, examples, and practice problems.",
            exercises=[
                Exercise(
                    id="interactive_001_ex1",
                    prompt="Create a multi-step learning prompt about any programming concept",
                    expected_intent=PromptIntent.HELP_ME_LEARN,
                    hints=["Use 'then' to chain steps", "Request quiz or practice"],
                    good_example="Explain recursion, provide examples, then quiz me to check understanding",
                    bad_example="Explain recursion"
                )
            ]
        )
        
        # Lesson 4: Socratic Method
        lesson4 = Lesson(
            id="socratic_001",
            title="Using the Socratic Method",
            description="Learn to ask reflective questions that deepen understanding.",
            learning_objectives=[
                "Ask 'why' and 'how' questions",
                "Request comparisons",
                "Explore relationships between concepts"
            ],
            difficulty=3,
            content="The Socratic method uses questions to explore concepts deeply and build understanding.",
            exercises=[
                Exercise(
                    id="socratic_001_ex1",
                    prompt="Create a reflective question about a programming concept",
                    expected_intent=PromptIntent.REFLECTION,
                    hints=["Use 'why', 'how', 'what if'", "Ask about relationships"],
                    good_example="How does inheritance relate to polymorphism, and why would I choose one over the other?",
                    bad_example="What is inheritance?"
                )
            ]
        )
        
        # Lesson 5: Advanced Techniques
        lesson5 = Lesson(
            id="advanced_001",
            title="Advanced Prompting Techniques",
            description="Master complex prompting strategies for deep learning.",
            learning_objectives=[
                "Combine multiple learning strategies",
                "Plan complete learning sessions",
                "Adapt prompts to learning goals"
            ],
            difficulty=4,
            content="Advanced prompting combines specificity, interactivity, and reflection for optimal learning.",
            exercises=[
                Exercise(
                    id="advanced_001_ex1",
                    prompt="Create a complete learning session prompt",
                    expected_intent=PromptIntent.HELP_ME_LEARN,
                    hints=["Combine explanation, examples, quiz, practice", "Be specific about the topic"],
                    good_example="Explain Python decorators with real-world examples, compare to similar patterns, quiz me on key concepts, then provide practice problems of increasing difficulty",
                    bad_example="Teach me decorators"
                )
            ]
        )
        
        # Add all lessons
        for lesson in [lesson1, lesson2, lesson3, lesson4, lesson5]:
            self.add_lesson(lesson)
