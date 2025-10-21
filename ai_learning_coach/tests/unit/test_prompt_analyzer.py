"""
Unit tests for PromptAnalyzer service.

Following TDD - tests written first to define expected behavior.
"""

import pytest
from src.services.prompt_analyzer import PromptAnalyzer
from src.services.score_strategies import RubricScorer
from src.models import PromptIntent, PromptAnalysis
from src.interfaces import IPromptEvaluator, IScoreStrategy


class TestPromptAnalyzer:
    """Test PromptAnalyzer implementation."""
    
    @pytest.mark.unit
    def test_prompt_analyzer_implements_interface(self):
        """Test that PromptAnalyzer implements IPromptEvaluator."""
        scorer = RubricScorer()
        analyzer = PromptAnalyzer(scorer)
        assert isinstance(analyzer, IPromptEvaluator)
    
    @pytest.mark.unit
    def test_analyze_good_learning_prompt(self):
        """Test analyzing a good learning-oriented prompt."""
        scorer = RubricScorer()
        analyzer = PromptAnalyzer(scorer)
        
        prompt = "Explain how recursion works in Python, then quiz me to verify my understanding"
        
        analysis = analyzer.evaluate(prompt)
        
        assert isinstance(analysis, PromptAnalysis)
        assert analysis.score.total_score >= 60
        assert analysis.score.intent == PromptIntent.HELP_ME_LEARN
        assert len(analysis.strengths) > 0
        assert len(analysis.detected_patterns) == 0
    
    @pytest.mark.unit
    def test_analyze_bad_do_it_for_me_prompt(self):
        """Test analyzing a 'do it for me' prompt."""
        scorer = RubricScorer()
        analyzer = PromptAnalyzer(scorer)
        
        prompt = "Write my code for me"
        
        analysis = analyzer.evaluate(prompt)
        
        assert analysis.score.total_score < 60
        assert analysis.score.intent == PromptIntent.DO_IT_FOR_ME
        assert len(analysis.detected_patterns) > 0
        # Check for the actual message pattern
        assert any("do-it-for-me" in pattern.lower() or "complete work" in pattern.lower() 
                   for pattern in analysis.detected_patterns)
    
    @pytest.mark.unit
    def test_detect_vague_language_anti_pattern(self):
        """Test detection of vague language anti-pattern."""
        scorer = RubricScorer()
        analyzer = PromptAnalyzer(scorer)
        
        prompt = "Help with stuff"
        
        analysis = analyzer.evaluate(prompt)
        
        assert len(analysis.detected_patterns) > 0
        assert any("vague" in pattern.lower() for pattern in analysis.detected_patterns)
    
    @pytest.mark.unit
    def test_detect_complete_solution_anti_pattern(self):
        """Test detection of requesting complete solutions."""
        scorer = RubricScorer()
        analyzer = PromptAnalyzer(scorer)
        
        prompt = "Give me the complete solution to this problem"
        
        analysis = analyzer.evaluate(prompt)
        
        assert len(analysis.detected_patterns) > 0
        assert any("complete" in pattern.lower() or "solution" in pattern.lower() 
                   for pattern in analysis.detected_patterns)
    
    @pytest.mark.unit
    def test_identify_strengths_specificity(self):
        """Test identification of specificity as a strength."""
        scorer = RubricScorer()
        analyzer = PromptAnalyzer(scorer)
        
        prompt = "Explain the difference between list comprehensions and generator expressions in Python, focusing on memory usage"
        
        analysis = analyzer.evaluate(prompt)
        
        assert len(analysis.strengths) > 0
        assert any("specific" in strength.lower() for strength in analysis.strengths)
    
    @pytest.mark.unit
    def test_identify_strengths_learning_oriented(self):
        """Test identification of learning orientation as a strength."""
        scorer = RubricScorer()
        analyzer = PromptAnalyzer(scorer)
        
        prompt = "Teach me about binary search trees with examples"
        
        analysis = analyzer.evaluate(prompt)
        
        assert len(analysis.strengths) > 0
        assert any("learn" in strength.lower() for strength in analysis.strengths)
    
    @pytest.mark.unit
    def test_identify_strengths_interactive(self):
        """Test identification of interactive elements as a strength."""
        scorer = RubricScorer()
        analyzer = PromptAnalyzer(scorer)
        
        prompt = "Explain inheritance, then quiz me on the concept"
        
        analysis = analyzer.evaluate(prompt)
        
        assert len(analysis.strengths) > 0
        assert any("interactive" in strength.lower() or "quiz" in strength.lower() 
                   for strength in analysis.strengths)
    
    @pytest.mark.unit
    def test_generate_improvements_for_low_score(self):
        """Test that improvements are suggested for low-scoring prompts."""
        scorer = RubricScorer()
        analyzer = PromptAnalyzer(scorer)
        
        prompt = "Do my homework"
        
        analysis = analyzer.evaluate(prompt)
        
        assert len(analysis.improvements) > 0
    
    @pytest.mark.unit
    def test_improvements_target_weak_dimensions(self):
        """Test that improvements target the weakest scoring dimensions."""
        scorer = RubricScorer()
        analyzer = PromptAnalyzer(scorer)
        
        # Vague prompt should get specificity improvement
        prompt = "Help"
        
        analysis = analyzer.evaluate(prompt)
        
        assert len(analysis.improvements) > 0
        # Should suggest being more specific since specificity is lowest
        assert any("specific" in imp.lower() or "detail" in imp.lower() 
                   for imp in analysis.improvements)
    
    @pytest.mark.unit
    def test_dependency_injection_different_scorer(self):
        """Test that analyzer works with different IScoreStrategy implementations."""
        # Create a mock scorer that always returns perfect scores
        class MockPerfectScorer(IScoreStrategy):
            def calculate_score(self, prompt: str):
                from src.models import PromptScore, PromptIntent
                return PromptScore(
                    total_score=100.0,
                    learning_orientation=100.0,
                    specificity=100.0,
                    engagement=100.0,
                    intent=PromptIntent.HELP_ME_LEARN
                )
        
        mock_scorer = MockPerfectScorer()
        analyzer = PromptAnalyzer(mock_scorer)
        
        analysis = analyzer.evaluate("any prompt")
        
        assert analysis.score.total_score == 100.0
        # Perfect score should have no improvements suggested
        assert len(analysis.improvements) == 0
    
    @pytest.mark.unit
    def test_empty_prompt_handling(self):
        """Test handling of empty prompts."""
        scorer = RubricScorer()
        analyzer = PromptAnalyzer(scorer)
        
        analysis = analyzer.evaluate("")
        
        assert analysis.score.total_score < 60
        assert len(analysis.detected_patterns) > 0
        assert len(analysis.improvements) > 0
    
    @pytest.mark.unit
    def test_very_long_prompt_handling(self):
        """Test handling of very long prompts."""
        scorer = RubricScorer()
        analyzer = PromptAnalyzer(scorer)
        
        # Create an excessively long prompt
        prompt = "Explain Python " * 100  # Very repetitive and long
        
        analysis = analyzer.evaluate(prompt)
        
        # Should still complete without error
        assert isinstance(analysis, PromptAnalysis)
        assert analysis.score is not None
