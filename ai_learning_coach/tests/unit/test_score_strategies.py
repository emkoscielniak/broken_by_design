"""
Unit tests for score strategies.

Following TDD - these tests verify the scoring logic.
"""

import pytest
from src.services.score_strategies import RubricScorer
from src.models import PromptIntent, PromptScore, ScoreWeights
from src.interfaces import IScoreStrategy


class TestRubricScorer:
    """Test RubricScorer implementation."""
    
    @pytest.mark.unit
    def test_rubric_scorer_implements_interface(self):
        """Test that RubricScorer implements IScoreStrategy."""
        scorer = RubricScorer()
        assert isinstance(scorer, IScoreStrategy)
    
    @pytest.mark.unit
    def test_score_good_learning_prompt(self):
        """Test scoring a good learning-oriented prompt."""
        scorer = RubricScorer()
        prompt = "Explain Python decorators with examples, then quiz me to check my understanding"
        
        score = scorer.calculate_score(prompt)
        
        assert isinstance(score, PromptScore)
        assert score.total_score > 60  # Should pass
        assert score.intent == PromptIntent.HELP_ME_LEARN
        assert score.learning_orientation > 60
    
    @pytest.mark.unit
    def test_score_bad_do_it_for_me_prompt(self):
        """Test scoring a 'do it for me' prompt."""
        scorer = RubricScorer()
        prompt = "Write my essay about climate change"
        
        score = scorer.calculate_score(prompt)
        
        assert isinstance(score, PromptScore)
        assert score.total_score < 60  # Should fail
        assert score.intent == PromptIntent.DO_IT_FOR_ME
        assert score.learning_orientation < 50
    
    @pytest.mark.unit
    def test_score_vague_prompt(self):
        """Test scoring a vague prompt."""
        scorer = RubricScorer()
        prompt = "Help me"
        
        score = scorer.calculate_score(prompt)
        
        assert score.specificity < 50  # Too vague
    
    @pytest.mark.unit
    def test_score_interactive_prompt(self):
        """Test scoring an interactive prompt."""
        scorer = RubricScorer()
        prompt = "Teach me about Python, quiz me on key concepts, then give me practice problems"
        
        score = scorer.calculate_score(prompt)
        
        assert score.engagement > 60  # Should be high engagement
        assert score.intent == PromptIntent.HELP_ME_LEARN
    
    @pytest.mark.unit
    def test_custom_weights(self):
        """Test using custom score weights."""
        custom_weights = ScoreWeights(
            learning_orientation=0.5,
            specificity=0.3,
            engagement=0.2
        )
        scorer = RubricScorer(weights=custom_weights)
        
        assert scorer.weights.learning_orientation == 0.5
        assert scorer.weights.specificity == 0.3
        assert scorer.weights.engagement == 0.2
    
    @pytest.mark.unit
    def test_classify_intent_do_it_for_me(self):
        """Test intent classification for 'do it for me'."""
        scorer = RubricScorer()
        
        prompts = [
            "Write my essay",
            "Do my homework",
            "Solve this for me",
            "Complete this assignment"
        ]
        
        for prompt in prompts:
            score = scorer.calculate_score(prompt)
            assert score.intent == PromptIntent.DO_IT_FOR_ME, f"Failed for: {prompt}"
    
    @pytest.mark.unit
    def test_classify_intent_help_me_learn(self):
        """Test intent classification for learning."""
        scorer = RubricScorer()
        
        prompts = [
            "Explain photosynthesis",
            "Teach me about Python",
            "Help me understand quantum physics",
            "Show me how to solve this",
            "Walk me through the steps"
        ]
        
        for prompt in prompts:
            score = scorer.calculate_score(prompt)
            assert score.intent == PromptIntent.HELP_ME_LEARN, f"Failed for: {prompt}"
    
    @pytest.mark.unit
    def test_classify_intent_clarifying(self):
        """Test intent classification for clarifying questions."""
        scorer = RubricScorer()
        
        prompts = [
            "What do you mean by polymorphism?",
            "Can you clarify that concept?",
            "What is the difference between X and Y?"
        ]
        
        for prompt in prompts:
            score = scorer.calculate_score(prompt)
            assert score.intent == PromptIntent.CLARIFYING, f"Failed for: {prompt}"
    
    @pytest.mark.unit
    def test_classify_intent_reflection(self):
        """Test intent classification for reflection."""
        scorer = RubricScorer()
        
        prompts = [
            "How does this relate to what we learned before?",
            "Why is this important?",
            "What if we tried a different approach?"
        ]
        
        for prompt in prompts:
            score = scorer.calculate_score(prompt)
            assert score.intent == PromptIntent.REFLECTION, f"Failed for: {prompt}"
    
    @pytest.mark.unit
    def test_score_ranges(self):
        """Test that all scores are in valid range 0-100."""
        scorer = RubricScorer()
        
        prompts = [
            "Write my code",
            "Explain everything",
            "Help me understand this specific concept about Python decorators",
            "Quiz me on what we just discussed, then give me harder problems"
        ]
        
        for prompt in prompts:
            score = scorer.calculate_score(prompt)
            assert 0 <= score.total_score <= 100
            assert 0 <= score.learning_orientation <= 100
            assert 0 <= score.specificity <= 100
            assert 0 <= score.engagement <= 100
    
    @pytest.mark.unit
    def test_learning_orientation_keywords(self):
        """Test learning orientation scoring with keywords."""
        scorer = RubricScorer()
        
        # Good keywords should increase score
        good_prompt = "Explain how recursion works and help me understand the base case"
        good_score = scorer._score_learning_orientation(good_prompt)
        
        # Bad keywords should decrease score
        bad_prompt = "Just tell me the answer and give me the solution"
        bad_score = scorer._score_learning_orientation(bad_prompt)
        
        assert good_score > bad_score
    
    @pytest.mark.unit
    def test_specificity_by_length(self):
        """Test that prompt length affects specificity score."""
        scorer = RubricScorer()
        
        short_prompt = "Help"
        medium_prompt = "Help me understand Python decorators and when to use them"
        
        short_score = scorer._score_specificity(short_prompt)
        medium_score = scorer._score_specificity(medium_prompt)
        
        assert medium_score > short_score
    
    @pytest.mark.unit
    def test_engagement_with_steps(self):
        """Test that multi-step prompts score higher on engagement."""
        scorer = RubricScorer()
        
        single_step = "Explain Python"
        multi_step = "Explain Python, then quiz me, then give me practice problems"
        
        single_score = scorer._score_engagement(single_step)
        multi_score = scorer._score_engagement(multi_step)
        
        assert multi_score > single_score
