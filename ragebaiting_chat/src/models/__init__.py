"""Models package initialization."""

from src.models.prompt_models import (
    PromptIntent,
    PromptScore,
    PromptAnalysis,
    Exercise,
    Lesson,
    UserProgress,
    CoachConfig,
    ScoreWeights,
    DemonstrationResult,
)

from src.models.ragebait_models import (
    EmotionalState,
    RageIndicator,
    InteractionAttempt,
    FrustrationScore,
    RageQuitResult,
    UserSession,
    PhilosophicalCommentary,
)

__all__ = [
    # Original models (keeping for backward compatibility)
    'PromptIntent',
    'PromptScore',
    'PromptAnalysis',
    'Exercise',
    'Lesson',
    'UserProgress',
    'CoachConfig',
    'ScoreWeights',
    'DemonstrationResult',
    # New ragebait models
    'EmotionalState',
    'RageIndicator',
    'InteractionAttempt',
    'FrustrationScore',
    'RageQuitResult',
    'UserSession',
    'PhilosophicalCommentary',
]
