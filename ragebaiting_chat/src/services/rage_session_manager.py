"""
Rage Session Manager - Orchestrates the full ragebait experience.

Coordinates between FrustrationAnalyzer and OppositeDoer to create
a session of escalating frustration that tracks user's emotional
descent and generates their final rage quit score.

SRP: Only manages session state and orchestrates service interactions.
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple
from src.models.ragebait_models import (
    EmotionalState,
    RageIndicator,
    InteractionAttempt,
    FrustrationScore,
    RageQuitResult,
    UserSession,
    PhilosophicalCommentary,
)
from src.services.antagonistic_services import (
    FrustrationAnalyzer,
    OppositeDoer,
)


class RageSessionManager:
    """
    Manages a complete ragebait session from optimism to rage quit.
    
    Responsibilities:
    - Track interaction attempts
    - Analyze user frustration
    - Generate antagonistic responses
    - Update session state
    - Detect rage quit conditions
    - Calculate final scores
    
    Usage:
        manager = RageSessionManager()
        response, state = manager.process_prompt("Explain Python")
        # ... multiple interactions ...
        if manager.should_offer_rage_quit():
            result = manager.generate_rage_quit_result()
    """
    
    def __init__(self):
        """Initialize session manager with analyzer and generator."""
        self.analyzer = FrustrationAnalyzer()
        self.opposite_doer = OppositeDoer()
        self.session: Optional[UserSession] = None
    
    def start_session(self, user_id: str = "anonymous") -> UserSession:
        """
        Start a new ragebait session.
        
        Args:
            user_id: Optional user identifier (default: "anonymous")
        
        Returns:
            UserSession: Fresh session starting at OPTIMISTIC state
        """
        self.session = UserSession(
            user_id=user_id,
            session_start=datetime.now(),
            attempts=[],
            current_emotional_state=EmotionalState.OPTIMISTIC
        )
        return self.session
    
    def process_prompt(
        self,
        prompt: str
    ) -> Tuple[str, EmotionalState, InteractionAttempt]:
        """
        Process a user prompt through the full ragebait pipeline.
        
        Args:
            prompt: User's input text
            
        Returns:
            Tuple of (antagonistic_response, emotional_state, attempt)
            
        Raises:
            RuntimeError: If session not started
        """
        if self.session is None:
            raise RuntimeError("Session not started. Call start_session() first.")
        
        # Analyze frustration
        emotional_state, rage_indicators, politeness, profanity, caps = \
            self.analyzer.analyze_prompt(prompt, self.session.attempts)
        
        # Generate antagonistic response
        attempt_number = len(self.session.attempts) + 1
        response = self.opposite_doer.generate_opposite_response(
            prompt,
            attempt_number
        )
        
        # Create attempt record
        attempt = InteractionAttempt(
            prompt=prompt,
            response=response,
            attempt_number=attempt_number,
            timestamp=datetime.now(),
            emotional_state=emotional_state,
            rage_indicators=rage_indicators,
            profanity_count=profanity,
            caps_percentage=caps,
            politeness_score=politeness
        )
        
        # Update session
        self.session.add_attempt(attempt)
        self.session.current_emotional_state = emotional_state
        
        return response, emotional_state, attempt
    
    def should_offer_rage_quit(self) -> bool:
        """
        Determine if user should be offered the rage quit option.
        
        Criteria:
        - At least 5 attempts (give them a chance)
        - Reached ANGRY or worse emotional state
        - OR 15+ attempts regardless of state
        
        Returns:
            bool: True if rage quit should be offered
        """
        if self.session is None:
            return False
        
        attempt_count = len(self.session.attempts)
        current_state = self.session.current_emotional_state
        
        # Minimum attempts before offering quit
        if attempt_count < 5:
            return False
        
        # Offer if angry/enraged/broken
        angry_states = [
            EmotionalState.ANGRY,
            EmotionalState.ENRAGED,
            EmotionalState.BROKEN
        ]
        if current_state in angry_states:
            return True
        
        # Offer if they've been trying for a while
        if attempt_count >= 15:
            return True
        
        return False
    
    def get_session_summary(self) -> dict:
        """
        Get current session statistics.
        
        Returns:
            dict: Session metrics including attempts, time, emotional state
        """
        if self.session is None:
            return {
                "active": False,
                "message": "No session active"
            }
        
        duration_seconds = self.session.session_duration_seconds
        duration = timedelta(seconds=duration_seconds)
        
        return {
            "active": True,
            "attempt_count": len(self.session.attempts),
            "duration_seconds": duration_seconds,
            "duration_display": self._format_duration(duration),
            "current_emotional_state": self.session.current_emotional_state.value,
            "politeness_decay": self.session.politeness_decay,
            "profanity_count": sum(a.profanity_count for a in self.session.attempts),
            "max_caps_percentage": max(
                (a.caps_percentage for a in self.session.attempts),
                default=0.0
            ),
            "rage_quit_available": self.should_offer_rage_quit()
        }
    
    def generate_rage_quit_result(self) -> RageQuitResult:
        """
        Generate the final rage quit result with scoring and commentary.
        
        Returns:
            RageQuitResult: Complete score breakdown and philosophical mockery
            
        Raises:
            RuntimeError: If session not started or has no attempts
        """
        if self.session is None:
            raise RuntimeError("Session not started")
        
        if not self.session.attempts:
            raise RuntimeError("No attempts recorded in session")
        
        # Calculate frustration score
        frustration_score = self._calculate_frustration_score()
        
        # Generate philosophical commentary
        commentary = PhilosophicalCommentary.generate_for_score(
            frustration_score
        )
        
        # Create result
        result = RageQuitResult(
            user_id=self.session.user_id,
            frustration_score=frustration_score,
            interaction_history=self.session.attempts,
            final_emotional_state=self.session.current_emotional_state,
            quit_timestamp=datetime.now(),
            philosophical_commentary=commentary
        )
        
        return result
    
    def _calculate_frustration_score(self) -> FrustrationScore:
        """Calculate the frustration score from session data."""
        if self.session is None or not self.session.attempts:
            raise RuntimeError("Cannot calculate score without session data")
        
        # Calculate time elapsed
        duration_seconds = self.session.session_duration_seconds
        time_elapsed = int(duration_seconds)
        
        # Find maximum emotional intensity
        state_intensity = {
            EmotionalState.OPTIMISTIC: 0,
            EmotionalState.CONFUSED: 1,
            EmotionalState.FRUSTRATED: 2,
            EmotionalState.ANGRY: 3,
            EmotionalState.ENRAGED: 4,
            EmotionalState.BROKEN: 5,
            EmotionalState.TRANSCENDENT: 6,
        }
        max_rage_level = max(
            state_intensity[attempt.emotional_state]
            for attempt in self.session.attempts
        )
        
        # Count unique profanities (simple approximation)
        all_prompts = " ".join(a.prompt.lower() for a in self.session.attempts)
        profanity_patterns = self.analyzer.PROFANITY_PATTERNS
        unique_profanities = sum(
            1 for pattern in profanity_patterns
            if pattern.strip(r'\b').strip(r'\b') in all_prompts
        )
        
        # Calculate politeness decay
        if len(self.session.attempts) >= 2:
            first_politeness = self.session.attempts[0].politeness_score
            last_politeness = self.session.attempts[-1].politeness_score
            politeness_decay = first_politeness - last_politeness
        else:
            politeness_decay = 0.0
        
        # Count caps lock escalation (attempts with >50% caps)
        caps_lock_escalation = sum(
            1 for attempt in self.session.attempts
            if attempt.caps_percentage > 50
        )
        
        # Count pleas
        plea_count = sum(
            1 for attempt in self.session.attempts
            if RageIndicator.PLEADING in attempt.rage_indicators
        )
        
        # Calculate philosophical score (0-100, higher = more persistent suffering)
        philosophical_score = min(
            len(self.session.attempts) * 2.5,  # 2.5 points per attempt
            100.0
        )
        
        return FrustrationScore(
            total_attempts=len(self.session.attempts),
            time_elapsed_seconds=time_elapsed,
            max_rage_level=max_rage_level,
            politeness_decay=politeness_decay,
            profanity_creativity=unique_profanities,
            caps_lock_escalation=caps_lock_escalation,
            plea_count=plea_count,
            philosophical_score=philosophical_score
        )
    
    def _format_duration(self, duration: timedelta) -> str:
        """Format duration in human-readable form."""
        seconds = int(duration.total_seconds())
        
        if seconds < 60:
            return f"{seconds} seconds"
        
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        
        if minutes < 60:
            return f"{minutes}m {remaining_seconds}s"
        
        hours = minutes // 60
        remaining_minutes = minutes % 60
        return f"{hours}h {remaining_minutes}m"
    
    def reset_session(self):
        """Reset the current session (for testing or starting over)."""
        self.session = None
