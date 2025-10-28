"""
Unit tests for data models.

Following TDD methodology - these tests drive the implementation.
"""

import pytest
from datetime import datetime
from src.models import (
    PromptIntent,
    PromptScore,
    PromptAnalysis,
    Exercise,
    Lesson,
    UserProgress,
    CoachConfig,
    ScoreWeights,
)


class TestPromptScore:
    """Test PromptScore model."""
    
    @pytest.mark.unit
    def test_prompt_score_creation(self):
        """Test creating a valid PromptScore."""
        score = PromptScore(
            total_score=75.0,
            learning_orientation=80.0,
            specificity=70.0,
            engagement=75.0,
            intent=PromptIntent.HELP_ME_LEARN
        )
        
        assert score.total_score == 75.0
        assert score.learning_orientation == 80.0
        assert score.specificity == 70.0
        assert score.engagement == 75.0
        assert score.intent == PromptIntent.HELP_ME_LEARN
    
    @pytest.mark.unit
    def test_is_passing_property_true(self):
        """Test is_passing returns True for score >= 60."""
        score = PromptScore(
            total_score=75.0,
            learning_orientation=80.0,
            specificity=70.0,
            engagement=75.0,
            intent=PromptIntent.HELP_ME_LEARN
        )
        assert score.is_passing is True
    
    @pytest.mark.unit
    def test_is_passing_property_false(self):
        """Test is_passing returns False for score < 60."""
        score = PromptScore(
            total_score=45.0,
            learning_orientation=50.0,
            specificity=40.0,
            engagement=45.0,
            intent=PromptIntent.DO_IT_FOR_ME
        )
        assert score.is_passing is False
    
    @pytest.mark.unit
    def test_is_passing_boundary(self):
        """Test is_passing at boundary (60.0)."""
        score = PromptScore(
            total_score=60.0,
            learning_orientation=60.0,
            specificity=60.0,
            engagement=60.0,
            intent=PromptIntent.UNKNOWN
        )
        assert score.is_passing is True
    
    @pytest.mark.unit
    def test_invalid_score_raises_error(self):
        """Test that invalid scores raise ValueError."""
        with pytest.raises(ValueError, match="total_score must be between 0 and 100"):
            PromptScore(
                total_score=150.0,  # Invalid
                learning_orientation=80.0,
                specificity=70.0,
                engagement=75.0,
                intent=PromptIntent.HELP_ME_LEARN
            )
    
    @pytest.mark.unit
    def test_negative_score_raises_error(self):
        """Test that negative scores raise ValueError."""
        with pytest.raises(ValueError, match="learning_orientation must be between 0 and 100"):
            PromptScore(
                total_score=75.0,
                learning_orientation=-10.0,  # Invalid
                specificity=70.0,
                engagement=75.0,
                intent=PromptIntent.HELP_ME_LEARN
            )


class TestPromptAnalysis:
    """Test PromptAnalysis model."""
    
    @pytest.mark.unit
    def test_prompt_analysis_creation(self):
        """Test creating a PromptAnalysis."""
        score = PromptScore(
            total_score=75.0,
            learning_orientation=80.0,
            specificity=70.0,
            engagement=75.0,
            intent=PromptIntent.HELP_ME_LEARN
        )
        
        analysis = PromptAnalysis(
            prompt="Explain Python and quiz me",
            score=score,
            strengths=["Learning-focused", "Specific"],
            improvements=["Add context"],
            examples=["Better example"],
            detected_patterns=[]
        )
        
        assert analysis.prompt == "Explain Python and quiz me"
        assert analysis.score == score
        assert len(analysis.strengths) == 2
        assert len(analysis.improvements) == 1
        assert len(analysis.detected_patterns) == 0


class TestLesson:
    """Test Lesson model."""
    
    @pytest.mark.unit
    def test_lesson_creation(self):
        """Test creating a valid Lesson."""
        lesson = Lesson(
            id="lesson_01",
            title="Introduction to Prompting",
            description="Learn the basics",
            learning_objectives=["Understand prompts", "Identify patterns"],
            difficulty=1,
            content="Lesson content here"
        )
        
        assert lesson.id == "lesson_01"
        assert lesson.title == "Introduction to Prompting"
        assert lesson.difficulty == 1
        assert len(lesson.learning_objectives) == 2
        assert len(lesson.exercises) == 0
    
    @pytest.mark.unit
    def test_lesson_with_exercises(self):
        """Test Lesson with exercises."""
        exercise = Exercise(
            id="ex_01",
            prompt="Transform this prompt",
            expected_intent=PromptIntent.HELP_ME_LEARN,
            hints=["Focus on learning"],
            good_example="Explain and quiz me",
            bad_example="Tell me the answer"
        )
        
        lesson = Lesson(
            id="lesson_01",
            title="Introduction",
            description="Description",
            learning_objectives=["Objective 1"],
            difficulty=2,
            content="Content",
            exercises=[exercise]
        )
        
        assert len(lesson.exercises) == 1
        assert lesson.exercises[0].id == "ex_01"
    
    @pytest.mark.unit
    def test_invalid_difficulty_raises_error(self):
        """Test that invalid difficulty raises ValueError."""
        with pytest.raises(ValueError, match="Difficulty must be between 1 and 5"):
            Lesson(
                id="lesson_01",
                title="Title",
                description="Description",
                learning_objectives=["Objective"],
                difficulty=6,  # Invalid
                content="Content"
            )


class TestUserProgress:
    """Test UserProgress model."""
    
    @pytest.mark.unit
    def test_user_progress_creation(self):
        """Test creating UserProgress."""
        progress = UserProgress(
            user_id="user_123",
            current_lesson=3,
            completed_lessons=["lesson_01", "lesson_02"],
            prompt_history=[],
            skill_level=2,
            total_prompts=10,
            good_prompts=8
        )
        
        assert progress.user_id == "user_123"
        assert progress.current_lesson == 3
        assert len(progress.completed_lessons) == 2
        assert progress.skill_level == 2
        assert progress.total_prompts == 10
        assert progress.good_prompts == 8
    
    @pytest.mark.unit
    def test_success_rate_calculation(self):
        """Test success rate property."""
        progress = UserProgress(
            user_id="user_123",
            current_lesson=1,
            completed_lessons=[],
            prompt_history=[],
            skill_level=1,
            total_prompts=10,
            good_prompts=8
        )
        
        assert progress.success_rate == 80.0
    
    @pytest.mark.unit
    def test_success_rate_zero_prompts(self):
        """Test success rate with zero prompts."""
        progress = UserProgress(
            user_id="user_123",
            current_lesson=1,
            completed_lessons=[],
            prompt_history=[],
            skill_level=1,
            total_prompts=0,
            good_prompts=0
        )
        
        assert progress.success_rate == 0.0
    
    @pytest.mark.unit
    def test_invalid_skill_level_raises_error(self):
        """Test that invalid skill level raises ValueError."""
        with pytest.raises(ValueError, match="Skill level must be between 1 and 5"):
            UserProgress(
                user_id="user_123",
                current_lesson=1,
                completed_lessons=[],
                prompt_history=[],
                skill_level=0,  # Invalid
                total_prompts=0,
                good_prompts=0
            )


class TestCoachConfig:
    """Test CoachConfig model."""
    
    @pytest.mark.unit
    def test_coach_config_creation(self):
        """Test creating CoachConfig with defaults."""
        config = CoachConfig(api_key="sk-test-key")
        
        assert config.api_key == "sk-test-key"
        assert config.model == "gpt-4o-mini"
        assert config.feedback_style == "detailed"
        assert config.auto_advance is False
        assert config.save_history is True
    
    @pytest.mark.unit
    def test_coach_config_custom_values(self):
        """Test creating CoachConfig with custom values."""
        config = CoachConfig(
            api_key="sk-test-key",
            model="gpt-4o",
            feedback_style="concise",
            auto_advance=True,
            save_history=False
        )
        
        assert config.model == "gpt-4o"
        assert config.feedback_style == "concise"
        assert config.auto_advance is True
        assert config.save_history is False
    
    @pytest.mark.unit
    def test_empty_api_key_raises_error(self):
        """Test that empty API key raises ValueError."""
        with pytest.raises(ValueError, match="API key cannot be empty"):
            CoachConfig(api_key="")
    
    @pytest.mark.unit
    def test_invalid_feedback_style_raises_error(self):
        """Test that invalid feedback style raises ValueError."""
        with pytest.raises(ValueError, match="feedback_style must be one of"):
            CoachConfig(
                api_key="sk-test-key",
                feedback_style="invalid"
            )


class TestScoreWeights:
    """Test ScoreWeights model."""
    
    @pytest.mark.unit
    def test_score_weights_defaults(self):
        """Test default weights."""
        weights = ScoreWeights()
        
        assert weights.learning_orientation == 0.4
        assert weights.specificity == 0.3
        assert weights.engagement == 0.3
    
    @pytest.mark.unit
    def test_score_weights_custom(self):
        """Test custom weights that sum to 1.0."""
        weights = ScoreWeights(
            learning_orientation=0.5,
            specificity=0.3,
            engagement=0.2
        )
        
        assert weights.learning_orientation == 0.5
        assert weights.specificity == 0.3
        assert weights.engagement == 0.2
    
    @pytest.mark.unit
    def test_invalid_weights_sum_raises_error(self):
        """Test that weights not summing to 1.0 raise ValueError."""
        with pytest.raises(ValueError, match="Weights must sum to 1.0"):
            ScoreWeights(
                learning_orientation=0.5,
                specificity=0.5,
                engagement=0.5  # Sum = 1.5, invalid
            )


class TestPromptIntent:
    """Test PromptIntent enum."""
    
    @pytest.mark.unit
    def test_prompt_intent_values(self):
        """Test PromptIntent enum values."""
        assert PromptIntent.DO_IT_FOR_ME.value == "do_it_for_me"
        assert PromptIntent.HELP_ME_LEARN.value == "help_me_learn"
        assert PromptIntent.CLARIFYING.value == "clarifying"
        assert PromptIntent.REFLECTION.value == "reflection"
        assert PromptIntent.UNKNOWN.value == "unknown"
