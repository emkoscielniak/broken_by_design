"""
Tests for PromptDemonstrator service.

Verifies:
- Pattern detection works correctly
- Simulated responses work without AI client
- Real API integration works with AI client
- Improved prompts are generated appropriately
- DemonstrationResult contains all required fields
"""

import pytest
from unittest.mock import Mock, MagicMock
from src.services import PromptDemonstrator
from src.models import DemonstrationResult


class TestPromptDemonstratorWithoutAI:
    """Test demonstrator in simulated mode (no AI client)."""
    
    def test_demonstrate_without_ai_client(self):
        """Should use simulated responses when no AI client provided."""
        demonstrator = PromptDemonstrator(ai_client=None)
        
        result = demonstrator.demonstrate("Write code for a calculator")
        
        assert isinstance(result, DemonstrationResult)
        assert result.is_simulated is True
        assert result.original_prompt == "Write code for a calculator"
        assert len(result.improved_prompt) > 0
        assert len(result.bad_response) > 0
        assert len(result.good_response) > 0
        assert len(result.explanation) > 0
    
    def test_detect_do_it_for_me_pattern(self):
        """Should detect 'do it for me' prompts."""
        demonstrator = PromptDemonstrator()
        
        prompts = [
            "Write code for a calculator",
            "Create a function to sort arrays",
            "Build a web app",
            "Generate HTML for a form",
        ]
        
        for prompt in prompts:
            pattern = demonstrator._detect_pattern(prompt)
            assert pattern == 'do_it_for_me'
    
    def test_detect_vague_pattern(self):
        """Should detect vague prompts (too short)."""
        demonstrator = PromptDemonstrator()
        
        prompts = [
            "Explain Python",
            "Help with JavaScript",
            "What is a class?",
        ]
        
        for prompt in prompts:
            pattern = demonstrator._detect_pattern(prompt)
            assert pattern == 'vague'
    
    def test_detect_no_context_pattern(self):
        """Should detect prompts about code that lack context."""
        demonstrator = PromptDemonstrator()
        
        # Need longer prompts with code keywords but no language/context
        prompts = [
            "My function returns an error when I run it",
            "The code doesn't work properly in my program",
            "How to fix this bug in my application code",
        ]
        
        for prompt in prompts:
            pattern = demonstrator._detect_pattern(prompt)
            # These might be detected as no_context or generic
            assert pattern in ['no_context', 'generic']
    
    def test_generate_improved_prompt_for_do_it_for_me(self):
        """Should generate learning-oriented improvements."""
        demonstrator = PromptDemonstrator()
        
        original = "Write code for a calculator"
        improved = demonstrator._generate_improved_prompt(original, 'do_it_for_me')
        
        # Improved prompt should have learning keywords
        assert 'explain' in improved.lower() or 'learn' in improved.lower()
        assert 'example' in improved.lower()
        assert len(improved) > len(original) * 2  # Should be more detailed
    
    def test_simulated_responses_exist_for_all_patterns(self):
        """Should have simulated responses for all pattern types."""
        demonstrator = PromptDemonstrator()
        patterns = ['do_it_for_me', 'vague', 'no_context', 'generic']
        
        for pattern in patterns:
            bad_response = demonstrator._get_simulated_bad_response(pattern)
            assert len(bad_response) > 0
            assert isinstance(bad_response, str)
    
    def test_demonstration_result_fields(self):
        """Should return complete DemonstrationResult."""
        demonstrator = PromptDemonstrator()
        
        result = demonstrator.demonstrate("Write a function")
        
        # Check all required fields
        assert hasattr(result, 'original_prompt')
        assert hasattr(result, 'improved_prompt')
        assert hasattr(result, 'bad_response')
        assert hasattr(result, 'good_response')
        assert hasattr(result, 'explanation')
        assert hasattr(result, 'is_simulated')
        
        # All fields should have content
        assert result.original_prompt
        assert result.improved_prompt
        assert result.bad_response
        assert result.good_response
        assert result.explanation


class TestPromptDemonstratorWithAI:
    """Test demonstrator with mocked AI client."""
    
    def test_demonstrate_with_ai_client(self):
        """Should use real API when AI client provided."""
        mock_ai = Mock()
        mock_ai.chat = Mock(side_effect=[
            "Minimal unhelpful response",
            "Detailed helpful educational response"
        ])
        
        demonstrator = PromptDemonstrator(ai_client=mock_ai)
        
        result = demonstrator.demonstrate("Explain Python decorators")
        
        # Should have called AI client twice (bad and good)
        assert mock_ai.chat.call_count == 2
        assert result.is_simulated is False
        assert "Minimal unhelpful response" in result.bad_response
        assert "Detailed helpful educational response" in result.good_response
    
    def test_bad_response_uses_unhelpful_system_prompt(self):
        """Should request unhelpful response for bad prompt."""
        mock_ai = Mock()
        mock_ai.chat = Mock(return_value="Mock response")
        
        demonstrator = PromptDemonstrator(ai_client=mock_ai)
        
        result = demonstrator.demonstrate("Test prompt")
        
        # Check first call (bad response) had unhelpful system prompt
        first_call_args = mock_ai.chat.call_args_list[0]
        messages = first_call_args[0][0]
        system_message = messages[0]
        
        assert system_message['role'] == 'system'
        assert 'minimal' in system_message['content'].lower() or 'unhelpful' in system_message['content'].lower()
    
    def test_good_response_uses_helpful_system_prompt(self):
        """Should request helpful response for improved prompt."""
        mock_ai = Mock()
        mock_ai.chat = Mock(side_effect=["Bad", "Good"])
        
        demonstrator = PromptDemonstrator(ai_client=mock_ai)
        
        result = demonstrator.demonstrate("Test prompt")
        
        # Check second call (good response) had helpful system prompt
        second_call_args = mock_ai.chat.call_args_list[1]
        messages = second_call_args[0][0]
        system_message = messages[0]
        
        assert system_message['role'] == 'system'
        assert 'coach' in system_message['content'].lower() or 'teach' in system_message['content'].lower()
    
    def test_fallback_to_simulated_on_api_error(self):
        """Should fall back to simulated if API fails."""
        mock_ai = Mock()
        mock_ai.chat = Mock(side_effect=Exception("API Error"))
        
        demonstrator = PromptDemonstrator(ai_client=mock_ai)
        
        result = demonstrator.demonstrate("Test prompt")
        
        # Should fall back to simulated
        assert result.is_simulated is True
        assert len(result.bad_response) > 0
        assert len(result.good_response) > 0
    
    def test_custom_improved_prompt(self):
        """Should use custom improved prompt when provided."""
        mock_ai = Mock()
        mock_ai.chat = Mock(side_effect=["Bad", "Good"])
        
        demonstrator = PromptDemonstrator(ai_client=mock_ai)
        
        custom_improved = "This is my custom improved version"
        result = demonstrator.demonstrate(
            "Original prompt",
            improved_prompt=custom_improved
        )
        
        assert result.improved_prompt == custom_improved
    
    def test_auto_generate_improved_when_not_provided(self):
        """Should auto-generate improved prompt when not provided."""
        demonstrator = PromptDemonstrator()
        
        original = "Write code"
        result = demonstrator.demonstrate(original)
        
        assert result.improved_prompt != original
        assert len(result.improved_prompt) > len(original)


class TestPatternDetectionEdgeCases:
    """Test edge cases in pattern detection."""
    
    def test_empty_prompt(self):
        """Should handle empty prompts gracefully."""
        demonstrator = PromptDemonstrator()
        
        result = demonstrator.demonstrate("")
        
        assert isinstance(result, DemonstrationResult)
        assert result.is_simulated is True
    
    def test_very_long_prompt(self):
        """Should handle long prompts."""
        demonstrator = PromptDemonstrator()
        
        long_prompt = "Explain " + "Python " * 100
        result = demonstrator.demonstrate(long_prompt)
        
        assert isinstance(result, DemonstrationResult)
    
    def test_prompt_with_mixed_intent(self):
        """Should classify prompts with mixed signals."""
        demonstrator = PromptDemonstrator()
        
        # Has both "write" (bad) and "explain" (good)
        mixed = "Write code to sort arrays and explain how it works"
        pattern = demonstrator._detect_pattern(mixed)
        
        # Should detect one of these patterns based on keywords
        assert pattern in ['do_it_for_me', 'no_context', 'generic']
    
    def test_good_prompt_classification(self):
        """Should handle already-good prompts."""
        demonstrator = PromptDemonstrator()
        
        good_prompt = "I'm learning Python decorators. Can you explain the concept with examples, then give me a practice problem to try?"
        pattern = demonstrator._detect_pattern(good_prompt)
        
        # Might be generic since it doesn't match specific bad patterns
        assert pattern in ['generic', 'do_it_for_me']


class TestExplanationGeneration:
    """Test explanation generation for different patterns."""
    
    def test_explanations_exist_for_all_patterns(self):
        """Should have explanations for all pattern types."""
        demonstrator = PromptDemonstrator()
        patterns = ['do_it_for_me', 'vague', 'no_context']
        
        for pattern in patterns:
            explanation = demonstrator._get_explanation(pattern)
            assert len(explanation) > 50  # Should be substantial
            assert '✅' in explanation  # Should have positive markers
    
    def test_explanation_mentions_key_improvements(self):
        """Should explain what makes improved version better."""
        demonstrator = PromptDemonstrator()
        
        result = demonstrator.demonstrate("Write code")
        
        # Explanation should mention key improvement areas
        explanation_lower = result.explanation.lower()
        improvement_keywords = ['explain', 'practice', 'understanding', 'learn', 'better']
        
        assert any(keyword in explanation_lower for keyword in improvement_keywords)
