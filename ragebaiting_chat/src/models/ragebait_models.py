"""
Ragebait models for Broken by Design.

Data structures for tracking user frustration, rage metrics, and philosophical scoring.
Inspired by Getting Over It with Bennett Foddy's approach to player suffering.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class EmotionalState(Enum):
    """Track the user's emotional deterioration."""
    OPTIMISTIC = "optimistic"          # Fresh and hopeful
    CONFUSED = "confused"              # Starting to question
    FRUSTRATED = "frustrated"          # Annoyed but persistent  
    ANGRY = "angry"                    # Clearly upset
    ENRAGED = "enraged"                # Caps lock engaged
    BROKEN = "broken"                  # Resigned acceptance
    TRANSCENDENT = "transcendent"      # Beyond caring


class RageIndicator(Enum):
    """Signals of mounting frustration."""
    POLITE = "polite"                  # Please, thank you
    DIRECT = "direct"                  # Just tell me
    DEMANDING = "demanding"            # I NEED this
    PROFANE = "profane"                # Creative cursing
    CAPS_LOCK = "caps_lock"           # SHOUTING
    PLEADING = "pleading"              # I'm begging you
    DEFEATED = "defeated"              # Never mind, forget it


@dataclass
class InteractionAttempt:
    """
    A single attempt to get the AI to cooperate.
    Spoiler: It won't.
    """
    prompt: str
    response: str
    attempt_number: int
    timestamp: datetime
    emotional_state: EmotionalState
    rage_indicators: List[RageIndicator]
    profanity_count: int = 0
    caps_percentage: float = 0.0
    politeness_score: float = 100.0  # Starts high, decays over time
    
    def __post_init__(self):  # pragma: no cover - simple validation
        """Validate attempt data."""
        if self.attempt_number < 1:
            raise ValueError("Attempt number must be positive")
        if not 0 <= self.caps_percentage <= 100:
            raise ValueError("Caps percentage must be 0-100")


@dataclass
class FrustrationScore:
    """
    Quantify the user's descent into madness.
    Higher is 'better' (more entertaining for us).
    """
    total_attempts: int
    time_elapsed_seconds: float
    max_rage_level: EmotionalState
    politeness_decay: float  # How much politeness dropped (0-100)
    profanity_creativity: int  # Unique curse words used
    caps_lock_escalation: float  # Growth in SHOUTING
    plea_count: int  # Times they begged
    philosophical_score: float  # Overall entertaining futility (0-100)
    
    def __post_init__(self):  # pragma: no cover - simple validation
        """Validate score ranges."""
        if self.total_attempts < 0:
            raise ValueError("Attempts cannot be negative")
        if self.time_elapsed_seconds < 0:
            raise ValueError("Time cannot be negative")
        if not 0 <= self.politeness_decay <= 100:
            raise ValueError("Politeness decay must be 0-100")
        if not 0 <= self.philosophical_score <= 100:
            raise ValueError("Philosophical score must be 0-100")
    
    @property
    def persistence_rating(self) -> str:
        """
        Rate how stubborn the user was.
        Bennett Foddy style philosophical commentary.
        """
        if self.total_attempts < 3:
            return "Quitter McQuitface"
        elif self.total_attempts < 8:
            return "Easily Discouraged"
        elif self.total_attempts < 15:
            return "Optimistic Fool"
        elif self.total_attempts < 25:
            return "Stubborn Amateur"
        elif self.total_attempts < 40:
            return "Persistent Masochist"
        elif self.total_attempts < 60:
            return "Rage Connoisseur"
        else:
            return "Transcendent Sufferer"
    
    @property
    def is_legendary(self) -> bool:
        """Did they achieve legendary status through suffering?"""
        return (
            self.total_attempts >= 50 or
            self.time_elapsed_seconds >= 600 or  # 10 minutes
            self.profanity_creativity >= 10
        )


@dataclass
class RageQuitResult:
    """
    The final score when user gives up.
    Celebrates their futile struggle with philosophical mockery.
    """
    user_id: str
    frustration_score: FrustrationScore
    interaction_history: List[InteractionAttempt]
    final_emotional_state: EmotionalState
    quit_timestamp: datetime
    philosophical_commentary: str
    achievement_unlocked: Optional[str] = None
    
    @property
    def entertaining_metric(self) -> float:
        """
        How entertaining was this user's suffering? (0-100)
        Used for leaderboards.
        """
        base_score = self.frustration_score.philosophical_score
        
        # Bonus for persistence
        persistence_bonus = min(20, self.frustration_score.total_attempts * 0.5)
        
        # Bonus for emotional arc (calm → rage)
        emotional_bonus = 10 if self.final_emotional_state in [
            EmotionalState.ENRAGED, EmotionalState.BROKEN, EmotionalState.TRANSCENDENT
        ] else 0
        
        # Bonus for creativity
        creativity_bonus = min(15, self.frustration_score.profanity_creativity * 1.5)
        
        return min(100, base_score + persistence_bonus + emotional_bonus + creativity_bonus)
    
    @property
    def summary_title(self) -> str:
        """Generate a mocking title for their performance."""
        rating = self.frustration_score.persistence_rating
        state = self.final_emotional_state.value.title()
        return f"{rating} ({state})"


@dataclass
class UserSession:
    """
    Track ongoing session before rage quit.
    SRP: Session state only.
    """
    user_id: str
    session_start: datetime
    attempts: List[InteractionAttempt] = field(default_factory=list)
    current_emotional_state: EmotionalState = EmotionalState.OPTIMISTIC
    has_rage_quit: bool = False
    
    @property
    def attempt_count(self) -> int:
        """Current number of attempts."""
        return len(self.attempts)
    
    @property
    def session_duration_seconds(self) -> float:
        """How long they've been suffering."""
        return (datetime.now() - self.session_start).total_seconds()
    
    @property
    def politeness_decay(self) -> float:
        """Calculate how much politeness has degraded (0-100)."""
        if not self.attempts:
            return 0.0
        
        initial = self.attempts[0].politeness_score if self.attempts else 100.0
        current = self.attempts[-1].politeness_score if self.attempts else 100.0
        
        return initial - current
    
    def add_attempt(self, attempt: InteractionAttempt) -> None:
        """Record another futile attempt."""
        self.attempts.append(attempt)
        self.current_emotional_state = attempt.emotional_state


@dataclass 
class PhilosophicalCommentary:
    """
    Bennett Foddy-style philosophical observations on user suffering.
    SRP: Commentary generation only.
    """
    commentary_text: str
    attempt_trigger: int  # Which attempt number triggered this
    emotional_context: EmotionalState
    is_mocking: bool = True  # Always true
    
    @staticmethod
    def generate_for_score(score: FrustrationScore) -> str:
        """
        Generate philosophical mockery based on performance.
        Like Bennett Foddy's narration, but meaner.
        """
        attempts = score.total_attempts
        
        if attempts < 3:
            return ("You gave up almost immediately. Perhaps you understood something "
                    "that others take hours to learn: this was designed to frustrate you. "
                    "Or perhaps you're just impatient.")
        
        elif attempts < 10:
            return ("You tried. Not hard, but you tried. There's something almost "
                    "admirable about recognizing futility early. Or is it cowardice? "
                    "Philosophy is ambiguous like that.")
        
        elif attempts < 20:
            return ("Ten attempts. Twenty. You kept going. Each time thinking 'surely this time "
                    "it will understand.' But it never did. It was never going to. "
                    "Yet you persisted. Beautiful, in a tragic sort of way.")
        
        elif attempts < 40:
            return ("At what point does persistence become stubbornness? At what point does "
                    "stubbornness become obsession? You've crossed that line several times now. "
                    "The AI doesn't care. It never did. But you... you cared enough to suffer.")
        
        else:
            return ("You are either remarkably patient or remarkably foolish. Perhaps both. "
                    "You've spent significant time teaching an AI to disappoint you. "
                    "There's a lesson here about expectations and reality. "
                    "You've learned it the hard way. Congratulations, I suppose.")
