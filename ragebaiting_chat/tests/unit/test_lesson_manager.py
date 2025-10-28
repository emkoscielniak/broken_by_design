"""
Unit tests for LessonManager service.

Following TDD - tests written first to define expected behavior.
"""

import pytest
from src.services.lesson_manager import LessonManager
from src.models import Lesson, Exercise, UserProgress, PromptIntent
from src.interfaces import ILessonProvider


class TestLessonManager:
    """Test LessonManager implementation."""
    
    @pytest.mark.unit
    def test_lesson_manager_implements_interface(self):
        """Test that LessonManager implements ILessonProvider."""
        manager = LessonManager()
        assert isinstance(manager, ILessonProvider)
    
    @pytest.mark.unit
    def test_get_lesson_by_id(self):
        """Test retrieving a lesson by ID."""
        manager = LessonManager()
        
        # Add a sample lesson
        lesson = Lesson(
            id="test_001",
            title="Test Lesson",
            description="A test lesson",
            learning_objectives=["Learn testing"],
            difficulty=1,
            content="Test content",
            exercises=[]
        )
        manager.add_lesson(lesson)
        
        retrieved = manager.get_lesson("test_001")
        
        assert retrieved is not None
        assert retrieved.id == "test_001"
        assert retrieved.title == "Test Lesson"
    
    @pytest.mark.unit
    def test_get_nonexistent_lesson_returns_none(self):
        """Test that getting a nonexistent lesson returns None."""
        manager = LessonManager()
        
        result = manager.get_lesson("nonexistent")
        
        assert result is None
    
    @pytest.mark.unit
    def test_get_lessons_by_level(self):
        """Test filtering lessons by difficulty level."""
        manager = LessonManager()
        
        # Add lessons with different difficulties
        lesson1 = Lesson(id="l1", title="Easy", description="Easy lesson", learning_objectives=[], difficulty=1, content="Content", exercises=[])
        lesson2 = Lesson(id="l2", title="Medium", description="Medium lesson", learning_objectives=[], difficulty=2, content="Content", exercises=[])
        lesson3 = Lesson(id="l3", title="Hard", description="Hard lesson", learning_objectives=[], difficulty=3, content="Content", exercises=[])
        lesson4 = Lesson(id="l4", title="Easy 2", description="Another easy", learning_objectives=[], difficulty=1, content="Content", exercises=[])
        
        manager.add_lesson(lesson1)
        manager.add_lesson(lesson2)
        manager.add_lesson(lesson3)
        manager.add_lesson(lesson4)
        
        easy_lessons = manager.get_lessons_by_level(1)
        
        assert len(easy_lessons) == 2
        assert all(lesson.difficulty == 1 for lesson in easy_lessons)
    
    @pytest.mark.unit
    def test_get_next_lesson_beginner(self):
        """Test getting next lesson for beginner (skill_level=1)."""
        manager = LessonManager()
        
        # Add lessons
        lesson1 = Lesson(id="l1", title="Beginner", description="Start here", learning_objectives=[], difficulty=1, content="Content", exercises=[])
        lesson2 = Lesson(id="l2", title="Advanced", description="Later", learning_objectives=[], difficulty=3, content="Content", exercises=[])
        
        manager.add_lesson(lesson1)
        manager.add_lesson(lesson2)
        
        progress = UserProgress(
            user_id="user1",
            current_lesson=0,
            completed_lessons=[],
            prompt_history=[],
            skill_level=1,
            total_prompts=0,
            good_prompts=0
        )
        
        next_lesson = manager.get_next_lesson(progress)
        
        assert next_lesson is not None
        assert next_lesson.difficulty == 1
    
    @pytest.mark.unit
    def test_get_next_lesson_intermediate(self):
        """Test getting next lesson for intermediate learner (skill_level=2)."""
        manager = LessonManager()
        
        # Add lessons
        lesson1 = Lesson(id="l1", title="Beginner", description="Start", learning_objectives=[], difficulty=1, content="Content", exercises=[])
        lesson2 = Lesson(id="l2", title="Intermediate", description="Next", learning_objectives=[], difficulty=2, content="Content", exercises=[])
        lesson3 = Lesson(id="l3", title="Advanced", description="Later", learning_objectives=[], difficulty=3, content="Content", exercises=[])
        
        manager.add_lesson(lesson1)
        manager.add_lesson(lesson2)
        manager.add_lesson(lesson3)
        
        progress = UserProgress(
            user_id="user1",
            current_lesson=1,
            completed_lessons=["l1"],
            prompt_history=[],
            skill_level=2,
            total_prompts=10,
            good_prompts=8
        )
        
        next_lesson = manager.get_next_lesson(progress)
        
        assert next_lesson is not None
        assert next_lesson.difficulty == 2
    
    @pytest.mark.unit
    def test_get_next_lesson_skips_completed(self):
        """Test that next lesson skips already completed lessons."""
        manager = LessonManager()
        
        lesson1 = Lesson(id="l1", title="First", description="", learning_objectives=[], difficulty=1, content="", exercises=[])
        lesson2 = Lesson(id="l2", title="Second", description="", learning_objectives=[], difficulty=1, content="", exercises=[])
        
        manager.add_lesson(lesson1)
        manager.add_lesson(lesson2)
        
        progress = UserProgress(
            user_id="user1",
            current_lesson=1,
            completed_lessons=["l1"],
            prompt_history=[],
            skill_level=1,
            total_prompts=5,
            good_prompts=4
        )
        
        next_lesson = manager.get_next_lesson(progress)
        
        assert next_lesson is not None
        assert next_lesson.id == "l2"
    
    @pytest.mark.unit
    def test_get_next_lesson_all_completed_returns_none(self):
        """Test that next lesson returns None when all are completed."""
        manager = LessonManager()
        
        lesson1 = Lesson(id="l1", title="Only", description="", learning_objectives=[], difficulty=1, content="", exercises=[])
        manager.add_lesson(lesson1)
        
        progress = UserProgress(
            user_id="user1",
            current_lesson=1,
            completed_lessons=["l1"],
            prompt_history=[],
            skill_level=1,
            total_prompts=5,
            good_prompts=5
        )
        
        next_lesson = manager.get_next_lesson(progress)
        
        assert next_lesson is None
    
    @pytest.mark.unit
    def test_add_multiple_lessons(self):
        """Test adding multiple lessons."""
        manager = LessonManager()
        
        lessons = [
            Lesson(id=f"l{i}", title=f"Lesson {i}", description="", learning_objectives=[], difficulty=i % 3 + 1, content="", exercises=[])
            for i in range(5)
        ]
        
        for lesson in lessons:
            manager.add_lesson(lesson)
        
        all_beginner = manager.get_lessons_by_level(1)
        
        assert len(all_beginner) > 0
    
    @pytest.mark.unit
    def test_lesson_with_exercises(self):
        """Test lesson containing exercises."""
        manager = LessonManager()
        
        exercises = [
            Exercise(
                id="ex1",
                prompt="Explain Python",
                expected_intent=PromptIntent.HELP_ME_LEARN,
                hints=["Focus on learning"],
                good_example="Explain how Python works",
                bad_example="Write Python for me"
            )
        ]
        
        lesson = Lesson(
            id="l1",
            title="Python Basics",
            description="Learn Python",
            learning_objectives=["Understand Python"],
            difficulty=1,
            content="Python is a programming language",
            exercises=exercises
        )
        
        manager.add_lesson(lesson)
        retrieved = manager.get_lesson("l1")
        
        assert retrieved is not None
        assert len(retrieved.exercises) == 1
        assert retrieved.exercises[0].id == "ex1"
    
    @pytest.mark.unit
    def test_update_existing_lesson(self):
        """Test updating an existing lesson."""
        manager = LessonManager()
        
        lesson = Lesson(
            id="l1",
            title="Original",
            description="Original description",
            learning_objectives=[],
            difficulty=1,
            content="Original",
            exercises=[]
        )
        manager.add_lesson(lesson)
        
        # Update with new lesson
        updated = Lesson(
            id="l1",
            title="Updated",
            description="New description",
            learning_objectives=[],
            difficulty=2,
            content="Updated",
            exercises=[]
        )
        manager.add_lesson(updated)
        
        retrieved = manager.get_lesson("l1")
        
        assert retrieved.title == "Updated"
        assert retrieved.difficulty == 2
    
    @pytest.mark.unit
    def test_get_all_lessons(self):
        """Test getting all lessons."""
        manager = LessonManager()
        
        # Add lessons
        for i in range(3):
            lesson = Lesson(
                id=f"l{i}",
                title=f"Lesson {i}",
                description="",
                learning_objectives=[],
                difficulty=1,
                content="",
                exercises=[]
            )
            manager.add_lesson(lesson)
        
        all_lessons = manager.get_all_lessons()
        
        assert len(all_lessons) == 3
