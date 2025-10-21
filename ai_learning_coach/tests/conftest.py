"""Test configuration and fixtures."""

import pytest
from unittest.mock import Mock
from src.models import PromptScore, PromptIntent, PromptAnalysis


@pytest.fixture
def sample_prompt_score():
    """Sample PromptScore for testing."""
    return PromptScore(
        total_score=75.0,
        learning_orientation=80.0,
        specificity=70.0,
        engagement=75.0,
        intent=PromptIntent.HELP_ME_LEARN
    )


@pytest.fixture
def sample_prompt_analysis(sample_prompt_score):
    """Sample PromptAnalysis for testing."""
    return PromptAnalysis(
        prompt="Explain Python decorators and quiz me",
        score=sample_prompt_score,
        strengths=["Learning-focused", "Specific topic"],
        improvements=["Could add more context"],
        examples=["Explain Python decorators with examples, then give me practice problems"],
        detected_patterns=[]
    )


@pytest.fixture
def bad_prompt_score():
    """Sample PromptScore for a bad prompt."""
    return PromptScore(
        total_score=25.0,
        learning_orientation=20.0,
        specificity=30.0,
        engagement=25.0,
        intent=PromptIntent.DO_IT_FOR_ME
    )


@pytest.fixture
def bad_prompt_analysis(bad_prompt_score):
    """Sample PromptAnalysis for a bad prompt."""
    return PromptAnalysis(
        prompt="Write my essay for me",
        score=bad_prompt_score,
        strengths=[],
        improvements=[
            "Focus on learning, not just getting answers",
            "Ask AI to teach you how to write, not write for you"
        ],
        examples=[
            "Explain how to structure an essay about climate change",
            "Help me brainstorm ideas for my essay and ask questions to develop my thinking"
        ],
        detected_patterns=["do_it_for_me"]
    )
