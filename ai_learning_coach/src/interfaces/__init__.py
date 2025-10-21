"""Interfaces package initialization."""

from src.interfaces.service_interfaces import (
    IPromptEvaluator,
    IScoreStrategy,
    ILessonProvider,
    IFeedbackProvider,
    IProgressPersister,
    IAIClient,
)

__all__ = [
    'IPromptEvaluator',
    'IScoreStrategy',
    'ILessonProvider',
    'IFeedbackProvider',
    'IProgressPersister',
    'IAIClient',
]
