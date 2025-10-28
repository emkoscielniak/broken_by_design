"""
Unit tests for FeedbackGenerator service.

Following TDD - tests written first to define expected behavior.
"""

import pytest
from src.services.feedback_generator import FeedbackGenerator
from src.models import PromptAnalysis, PromptScore, PromptIntent
from src.interfaces import IFeedbackProvider


class TestFeedbackGenerator:
    """Test FeedbackGenerator implementation."""
    
    @pytest.mark.unit
    def test_feedback_generator_implements_interface(self):
        """Test that FeedbackGenerator implements IFeedbackProvider."""
        generator = FeedbackGenerator()
        assert isinstance(generator, IFeedbackProvider)
    
    @pytest.mark.unit
    def test_generate_encouraging_feedback(self):
        """Test generating encouraging feedback style."""
        generator = FeedbackGenerator(style="encouraging")
        
        analysis = PromptAnalysis(
            prompt="Explain Python decorators",
            score=PromptScore(
                total_score=75.0,
                learning_orientation=80.0,
                specificity=70.0,
                engagement=75.0,
                intent=PromptIntent.HELP_ME_LEARN
            ),
            strengths=["Learning-oriented approach"],
            improvements=["Add interactive elements"],
            examples=["Try adding: quiz me"],
            detected_patterns=[]
        )
        
        feedback = generator.generate_feedback(analysis)
        
        assert isinstance(feedback, str)
        assert len(feedback) > 0
        # Encouraging style should be positive
        assert any(word in feedback.lower() for word in ["great", "good", "excellent", "nice"])
    
    @pytest.mark.unit
    def test_generate_direct_feedback(self):
        """Test generating direct feedback style."""
        generator = FeedbackGenerator(style="direct")
        
        analysis = PromptAnalysis(
            prompt="Do my homework",
            score=PromptScore(
                total_score=25.0,
                learning_orientation=20.0,
                specificity=30.0,
                engagement=25.0,
                intent=PromptIntent.DO_IT_FOR_ME
            ),
            strengths=[],
            improvements=["Rephrase to focus on learning"],
            examples=["Instead of 'Do my homework', try 'Teach me the concepts'"],
            detected_patterns=["Do-it-for-me pattern detected"]
        )
        
        feedback = generator.generate_feedback(analysis)
        
        assert isinstance(feedback, str)
        assert len(feedback) > 0
        # Direct style should be straightforward
        assert "score" in feedback.lower() or "needs" in feedback.lower()
    
    @pytest.mark.unit
    def test_generate_socratic_feedback(self):
        """Test generating Socratic feedback style."""
        generator = FeedbackGenerator(style="socratic")
        
        analysis = PromptAnalysis(
            prompt="Help with coding",
            score=PromptScore(
                total_score=45.0,
                learning_orientation=50.0,
                specificity=30.0,
                engagement=55.0,
                intent=PromptIntent.HELP_ME_LEARN
            ),
            strengths=["Learning-oriented"],
            improvements=["Be more specific"],
            examples=["What specific coding topic?"],
            detected_patterns=["Vague language"]
        )
        
        feedback = generator.generate_feedback(analysis)
        
        assert isinstance(feedback, str)
        assert len(feedback) > 0
        # Socratic style should ask questions
        assert "?" in feedback
    
    @pytest.mark.unit
    def test_feedback_includes_score(self):
        """Test that feedback includes the score."""
        generator = FeedbackGenerator()
        
        analysis = PromptAnalysis(
            prompt="Test prompt",
            score=PromptScore(
                total_score=65.0,
                learning_orientation=70.0,
                specificity=60.0,
                engagement=65.0,
                intent=PromptIntent.HELP_ME_LEARN
            ),
            strengths=["Good attempt"],
            improvements=[],
            examples=[],
            detected_patterns=[]
        )
        
        feedback = generator.generate_feedback(analysis)
        
        # Should mention the score
        assert "65" in feedback or "score" in feedback.lower()
    
    @pytest.mark.unit
    def test_feedback_includes_strengths(self):
        """Test that feedback includes identified strengths."""
        generator = FeedbackGenerator()
        
        analysis = PromptAnalysis(
            prompt="Explain recursion with examples, then quiz me",
            score=PromptScore(
                total_score=85.0,
                learning_orientation=90.0,
                specificity=80.0,
                engagement=85.0,
                intent=PromptIntent.HELP_ME_LEARN
            ),
            strengths=["Learning-oriented approach", "Interactive learning requested"],
            improvements=[],
            examples=[],
            detected_patterns=[]
        )
        
        feedback = generator.generate_feedback(analysis)
        
        # Should mention strengths
        assert "learning-oriented" in feedback.lower() or "interactive" in feedback.lower()
    
    @pytest.mark.unit
    def test_feedback_includes_improvements(self):
        """Test that feedback includes improvement suggestions."""
        generator = FeedbackGenerator()
        
        analysis = PromptAnalysis(
            prompt="Help",
            score=PromptScore(
                total_score=30.0,
                learning_orientation=40.0,
                specificity=20.0,
                engagement=30.0,
                intent=PromptIntent.UNKNOWN
            ),
            strengths=[],
            improvements=["Add more specific details", "Expand your prompt"],
            examples=["Instead of 'Help', try 'Explain X'"],
            detected_patterns=["Very short prompt"]
        )
        
        feedback = generator.generate_feedback(analysis)
        
        # Should mention improvements
        assert "specific" in feedback.lower() or "improve" in feedback.lower()
    
    @pytest.mark.unit
    def test_feedback_includes_anti_patterns(self):
        """Test that feedback mentions detected anti-patterns."""
        generator = FeedbackGenerator()
        
        analysis = PromptAnalysis(
            prompt="Write my essay",
            score=PromptScore(
                total_score=20.0,
                learning_orientation=10.0,
                specificity=30.0,
                engagement=20.0,
                intent=PromptIntent.DO_IT_FOR_ME
            ),
            strengths=[],
            improvements=["Shift from 'do it for me' to 'teach me how'"],
            examples=["Instead of 'Write my essay', try 'Help me structure my thoughts'"],
            detected_patterns=["Do-it-for-me pattern detected"]
        )
        
        feedback = generator.generate_feedback(analysis)
        
        # Should mention the anti-pattern
        assert "do-it-for-me" in feedback.lower() or "pattern" in feedback.lower()
    
    @pytest.mark.unit
    def test_feedback_includes_examples(self):
        """Test that feedback includes example prompts."""
        generator = FeedbackGenerator()
        
        analysis = PromptAnalysis(
            prompt="Vague request",
            score=PromptScore(
                total_score=35.0,
                learning_orientation=40.0,
                specificity=25.0,
                engagement=40.0,
                intent=PromptIntent.HELP_ME_LEARN
            ),
            strengths=[],
            improvements=["Be more specific"],
            examples=["Instead of 'Vague request', try 'Explain X with examples'"],
            detected_patterns=[]
        )
        
        feedback = generator.generate_feedback(analysis)
        
        # Should include examples
        assert "instead" in feedback.lower() or "try" in feedback.lower() or "example" in feedback.lower()
    
    @pytest.mark.unit
    def test_change_feedback_style(self):
        """Test changing feedback style after initialization."""
        generator = FeedbackGenerator(style="encouraging")
        
        analysis = PromptAnalysis(
            prompt="Test",
            score=PromptScore(
                total_score=50.0,
                learning_orientation=50.0,
                specificity=50.0,
                engagement=50.0,
                intent=PromptIntent.HELP_ME_LEARN
            ),
            strengths=[],
            improvements=[],
            examples=[],
            detected_patterns=[]
        )
        
        encouraging_feedback = generator.generate_feedback(analysis)
        
        # Change style
        generator.style = "direct"
        direct_feedback = generator.generate_feedback(analysis)
        
        # Feedback should be different
        assert encouraging_feedback != direct_feedback
    
    @pytest.mark.unit
    def test_invalid_style_defaults_to_encouraging(self):
        """Test that invalid style defaults to encouraging."""
        generator = FeedbackGenerator(style="invalid_style")
        
        # Should default to encouraging without error
        assert generator.style in ["encouraging", "direct", "socratic"]
    
    @pytest.mark.unit
    def test_high_score_feedback_is_positive(self):
        """Test that high-scoring prompts get positive feedback."""
        generator = FeedbackGenerator()
        
        analysis = PromptAnalysis(
            prompt="Excellent prompt",
            score=PromptScore(
                total_score=95.0,
                learning_orientation=95.0,
                specificity=95.0,
                engagement=95.0,
                intent=PromptIntent.HELP_ME_LEARN
            ),
            strengths=["Learning-oriented", "Specific", "Interactive"],
            improvements=[],
            examples=[],
            detected_patterns=[]
        )
        
        feedback = generator.generate_feedback(analysis)
        
        # High scores should get positive feedback
        assert any(word in feedback.lower() for word in ["excellent", "great", "outstanding", "strong"])
