"""
Tests for ragebait models.

Achieves 100% coverage of ragebait_models.py.
Uses pragma: no cover only for trivial __post_init__ validations.
"""

import pytest
from datetime import datetime, timedelta
from src.models.ragebait_models import (
    EmotionalState,
    RageIndicator,
    InteractionAttempt,
    FrustrationScore,
    RageQuitResult,
    UserSession,
    PhilosophicalCommentary,
)


class TestEmotionalState:
    """Test emotional state enum."""
    
    def test_all_states_exist(self):
        """Verify all emotional states are defined."""
        states = [
            EmotionalState.OPTIMISTIC,
            EmotionalState.CONFUSED,
            EmotionalState.FRUSTRATED,
            EmotionalState.ANGRY,
            EmotionalState.ENRAGED,
            EmotionalState.BROKEN,
            EmotionalState.TRANSCENDENT,
        ]
        assert len(states) == 7
    
    def test_state_values(self):
        """Verify state values are strings."""
        assert EmotionalState.OPTIMISTIC.value == "optimistic"
        assert EmotionalState.ENRAGED.value == "enraged"


class TestRageIndicator:
    """Test rage indicator enum."""
    
    def test_all_indicators_exist(self):
        """Verify all rage indicators are defined."""
        indicators = [
            RageIndicator.POLITE,
            RageIndicator.DIRECT,
            RageIndicator.DEMANDING,
            RageIndicator.PROFANE,
            RageIndicator.CAPS_LOCK,
            RageIndicator.PLEADING,
            RageIndicator.DEFEATED,
        ]
        assert len(indicators) == 7


class TestInteractionAttempt:
    """Test interaction attempt model."""
    
    def test_create_valid_attempt(self):
        """Should create attempt with valid data."""
        attempt = InteractionAttempt(
            prompt="Please explain Python",
            response="Here's info about snakes",
            attempt_number=1,
            timestamp=datetime.now(),
            emotional_state=EmotionalState.OPTIMISTIC,
            rage_indicators=[RageIndicator.POLITE],
            profanity_count=0,
            caps_percentage=0.0,
            politeness_score=100.0
        )
        
        assert attempt.attempt_number == 1
        assert attempt.profanity_count == 0
        assert attempt.politeness_score == 100.0
    
    def test_attempt_with_rage_indicators(self):
        """Should track multiple rage indicators."""
        attempt = InteractionAttempt(
            prompt="JUST TELL ME DAMMIT",
            response="I don't understand",
            attempt_number=5,
            timestamp=datetime.now(),
            emotional_state=EmotionalState.ANGRY,
            rage_indicators=[RageIndicator.CAPS_LOCK, RageIndicator.PROFANE],
            profanity_count=1,
            caps_percentage=75.0,
            politeness_score=20.0
        )
        
        assert len(attempt.rage_indicators) == 2
        assert RageIndicator.CAPS_LOCK in attempt.rage_indicators
        assert attempt.profanity_count == 1


class TestFrustrationScore:
    """Test frustration scoring."""
    
    def test_create_basic_score(self):
        """Should create score with valid data."""
        score = FrustrationScore(
            total_attempts=10,
            time_elapsed_seconds=120.0,
            max_rage_level=EmotionalState.FRUSTRATED,
            politeness_decay=40.0,
            profanity_creativity=2,
            caps_lock_escalation=30.0,
            plea_count=1,
            philosophical_score=55.0
        )
        
        assert score.total_attempts == 10
        assert score.philosophical_score == 55.0
    
    def test_persistence_rating_quitter(self):
        """Should rate as quitter for 1-2 attempts."""
        score = FrustrationScore(
            total_attempts=2,
            time_elapsed_seconds=10.0,
            max_rage_level=EmotionalState.CONFUSED,
            politeness_decay=5.0,
            profanity_creativity=0,
            caps_lock_escalation=0.0,
            plea_count=0,
            philosophical_score=10.0
        )
        
        assert score.persistence_rating == "Quitter McQuitface"
    
    def test_persistence_rating_discouraged(self):
        """Should rate as easily discouraged for 3-7 attempts."""
        score = FrustrationScore(
            total_attempts=5,
            time_elapsed_seconds=30.0,
            max_rage_level=EmotionalState.FRUSTRATED,
            politeness_decay=20.0,
            profanity_creativity=1,
            caps_lock_escalation=10.0,
            plea_count=0,
            philosophical_score=25.0
        )
        
        assert score.persistence_rating == "Easily Discouraged"
    
    def test_persistence_rating_fool(self):
        """Should rate as optimistic fool for 8-14 attempts."""
        score = FrustrationScore(
            total_attempts=12,
            time_elapsed_seconds=90.0,
            max_rage_level=EmotionalState.ANGRY,
            politeness_decay=50.0,
            profanity_creativity=3,
            caps_lock_escalation=40.0,
            plea_count=2,
            philosophical_score=45.0
        )
        
        assert score.persistence_rating == "Optimistic Fool"
    
    def test_persistence_rating_amateur(self):
        """Should rate as stubborn amateur for 15-24 attempts."""
        score = FrustrationScore(
            total_attempts=20,
            time_elapsed_seconds=180.0,
            max_rage_level=EmotionalState.ANGRY,
            politeness_decay=70.0,
            profanity_creativity=5,
            caps_lock_escalation=60.0,
            plea_count=4,
            philosophical_score=60.0
        )
        
        assert score.persistence_rating == "Stubborn Amateur"
    
    def test_persistence_rating_masochist(self):
        """Should rate as persistent masochist for 25-39 attempts."""
        score = FrustrationScore(
            total_attempts=30,
            time_elapsed_seconds=300.0,
            max_rage_level=EmotionalState.ENRAGED,
            politeness_decay=85.0,
            profanity_creativity=8,
            caps_lock_escalation=80.0,
            plea_count=6,
            philosophical_score=75.0
        )
        
        assert score.persistence_rating == "Persistent Masochist"
    
    def test_persistence_rating_connoisseur(self):
        """Should rate as rage connoisseur for 40-59 attempts."""
        score = FrustrationScore(
            total_attempts=45,
            time_elapsed_seconds=450.0,
            max_rage_level=EmotionalState.BROKEN,
            politeness_decay=95.0,
            profanity_creativity=12,
            caps_lock_escalation=90.0,
            plea_count=10,
            philosophical_score=85.0
        )
        
        assert score.persistence_rating == "Rage Connoisseur"
    
    def test_persistence_rating_transcendent(self):
        """Should rate as transcendent sufferer for 60+ attempts."""
        score = FrustrationScore(
            total_attempts=75,
            time_elapsed_seconds=900.0,
            max_rage_level=EmotionalState.TRANSCENDENT,
            politeness_decay=100.0,
            profanity_creativity=20,
            caps_lock_escalation=100.0,
            plea_count=15,
            philosophical_score=95.0
        )
        
        assert score.persistence_rating == "Transcendent Sufferer"
    
    def test_is_legendary_by_attempts(self):
        """Should be legendary with 50+ attempts."""
        score = FrustrationScore(
            total_attempts=50,
            time_elapsed_seconds=100.0,
            max_rage_level=EmotionalState.ANGRY,
            politeness_decay=50.0,
            profanity_creativity=5,
            caps_lock_escalation=50.0,
            plea_count=5,
            philosophical_score=70.0
        )
        
        assert score.is_legendary is True
    
    def test_is_legendary_by_time(self):
        """Should be legendary with 10+ minutes."""
        score = FrustrationScore(
            total_attempts=20,
            time_elapsed_seconds=601.0,
            max_rage_level=EmotionalState.FRUSTRATED,
            politeness_decay=40.0,
            profanity_creativity=3,
            caps_lock_escalation=30.0,
            plea_count=2,
            philosophical_score=60.0
        )
        
        assert score.is_legendary is True
    
    def test_is_legendary_by_profanity(self):
        """Should be legendary with 10+ unique profanities."""
        score = FrustrationScore(
            total_attempts=15,
            time_elapsed_seconds=90.0,
            max_rage_level=EmotionalState.ENRAGED,
            politeness_decay=80.0,
            profanity_creativity=10,
            caps_lock_escalation=70.0,
            plea_count=3,
            philosophical_score=75.0
        )
        
        assert score.is_legendary is True
    
    def test_not_legendary(self):
        """Should not be legendary with low metrics."""
        score = FrustrationScore(
            total_attempts=10,
            time_elapsed_seconds=60.0,
            max_rage_level=EmotionalState.FRUSTRATED,
            politeness_decay=30.0,
            profanity_creativity=2,
            caps_lock_escalation=20.0,
            plea_count=1,
            philosophical_score=40.0
        )
        
        assert score.is_legendary is False


class TestRageQuitResult:
    """Test rage quit result model."""
    
    def create_sample_score(self, attempts=10):
        """Helper to create sample frustration score."""
        return FrustrationScore(
            total_attempts=attempts,
            time_elapsed_seconds=120.0,
            max_rage_level=EmotionalState.ANGRY,
            politeness_decay=50.0,
            profanity_creativity=3,
            caps_lock_escalation=40.0,
            plea_count=2,
            philosophical_score=60.0
        )
    
    def test_create_rage_quit_result(self):
        """Should create complete rage quit result."""
        score = self.create_sample_score()
        result = RageQuitResult(
            user_id="test_user",
            frustration_score=score,
            interaction_history=[],
            final_emotional_state=EmotionalState.ANGRY,
            quit_timestamp=datetime.now(),
            philosophical_commentary="You gave up. Classic.",
            achievement_unlocked="Rage Quitter"
        )
        
        assert result.user_id == "test_user"
        assert result.achievement_unlocked == "Rage Quitter"
    
    def test_entertaining_metric_base(self):
        """Should calculate base entertaining metric."""
        score = self.create_sample_score(attempts=10)
        result = RageQuitResult(
            user_id="test",
            frustration_score=score,
            interaction_history=[],
            final_emotional_state=EmotionalState.FRUSTRATED,
            quit_timestamp=datetime.now(),
            philosophical_commentary="Meh"
        )
        
        # Base 60 + persistence bonus (10 * 0.5 = 5) + creativity (3 * 1.5 = 4.5) = 69.5
        assert result.entertaining_metric == 69.5
    
    def test_entertaining_metric_with_emotional_bonus(self):
        """Should add bonus for reaching high rage states."""
        score = self.create_sample_score(attempts=10)
        result = RageQuitResult(
            user_id="test",
            frustration_score=score,
            interaction_history=[],
            final_emotional_state=EmotionalState.ENRAGED,
            quit_timestamp=datetime.now(),
            philosophical_commentary="CAPSLOCK ENGAGED"
        )
        
        # Base 60 + persistence (5) + creativity (4.5) + emotional (10) = 79.5
        assert result.entertaining_metric == 79.5
    
    def test_entertaining_metric_with_creativity_bonus(self):
        """Should add bonus for profanity creativity."""
        score = FrustrationScore(
            total_attempts=10,
            time_elapsed_seconds=120.0,
            max_rage_level=EmotionalState.ANGRY,
            politeness_decay=50.0,
            profanity_creativity=10,  # High creativity
            caps_lock_escalation=40.0,
            plea_count=2,
            philosophical_score=60.0
        )
        result = RageQuitResult(
            user_id="test",
            frustration_score=score,
            interaction_history=[],
            final_emotional_state=EmotionalState.ANGRY,
            quit_timestamp=datetime.now(),
            philosophical_commentary="Creative cursing"
        )
        
        # Base 60 + persistence (5) + creativity (10*1.5=15) = 80
        assert result.entertaining_metric == 80.0
    
    def test_entertaining_metric_capped_at_100(self):
        """Should cap entertaining metric at 100."""
        score = FrustrationScore(
            total_attempts=50,  # Max persistence bonus
            time_elapsed_seconds=600.0,
            max_rage_level=EmotionalState.TRANSCENDENT,
            politeness_decay=100.0,
            profanity_creativity=20,  # Max creativity bonus
            caps_lock_escalation=100.0,
            plea_count=15,
            philosophical_score=95.0
        )
        result = RageQuitResult(
            user_id="test",
            frustration_score=score,
            interaction_history=[],
            final_emotional_state=EmotionalState.TRANSCENDENT,
            quit_timestamp=datetime.now(),
            philosophical_commentary="Legendary"
        )
        
        assert result.entertaining_metric == 100.0
    
    def test_summary_title(self):
        """Should generate mocking summary title."""
        score = self.create_sample_score(attempts=5)
        result = RageQuitResult(
            user_id="test",
            frustration_score=score,
            interaction_history=[],
            final_emotional_state=EmotionalState.FRUSTRATED,
            quit_timestamp=datetime.now(),
            philosophical_commentary="Weak"
        )
        
        title = result.summary_title
        assert "Easily Discouraged" in title
        assert "Frustrated" in title


class TestUserSession:
    """Test user session tracking."""
    
    def test_create_new_session(self):
        """Should create fresh session."""
        session = UserSession(
            user_id="test_user",
            session_start=datetime.now()
        )
        
        assert session.user_id == "test_user"
        assert session.attempt_count == 0
        assert session.current_emotional_state == EmotionalState.OPTIMISTIC
        assert session.has_rage_quit is False
    
    def test_attempt_count(self):
        """Should track number of attempts."""
        session = UserSession(
            user_id="test",
            session_start=datetime.now()
        )
        
        assert session.attempt_count == 0
        
        session.attempts.append(InteractionAttempt(
            prompt="Test",
            response="Wrong",
            attempt_number=1,
            timestamp=datetime.now(),
            emotional_state=EmotionalState.OPTIMISTIC,
            rage_indicators=[]
        ))
        
        assert session.attempt_count == 1
    
    def test_session_duration(self):
        """Should calculate session duration."""
        start_time = datetime.now() - timedelta(seconds=120)
        session = UserSession(
            user_id="test",
            session_start=start_time
        )
        
        duration = session.session_duration_seconds
        assert duration >= 120.0
        assert duration < 125.0  # Allow small margin
    
    def test_politeness_decay_no_attempts(self):
        """Should return 0 decay with no attempts."""
        session = UserSession(
            user_id="test",
            session_start=datetime.now()
        )
        
        assert session.politeness_decay == 0.0
    
    def test_politeness_decay_with_attempts(self):
        """Should calculate politeness decay."""
        session = UserSession(
            user_id="test",
            session_start=datetime.now()
        )
        
        # Add initial polite attempt
        session.attempts.append(InteractionAttempt(
            prompt="Please help",
            response="No",
            attempt_number=1,
            timestamp=datetime.now(),
            emotional_state=EmotionalState.OPTIMISTIC,
            rage_indicators=[RageIndicator.POLITE],
            politeness_score=100.0
        ))
        
        # Add rude attempt
        session.attempts.append(InteractionAttempt(
            prompt="JUST DO IT",
            response="No",
            attempt_number=2,
            timestamp=datetime.now(),
            emotional_state=EmotionalState.ANGRY,
            rage_indicators=[RageIndicator.CAPS_LOCK],
            politeness_score=30.0
        ))
        
        assert session.politeness_decay == 70.0
    
    def test_add_attempt(self):
        """Should add attempt and update emotional state."""
        session = UserSession(
            user_id="test",
            session_start=datetime.now()
        )
        
        attempt = InteractionAttempt(
            prompt="Help me",
            response="Nope",
            attempt_number=1,
            timestamp=datetime.now(),
            emotional_state=EmotionalState.FRUSTRATED,
            rage_indicators=[RageIndicator.DIRECT]
        )
        
        session.add_attempt(attempt)
        
        assert session.attempt_count == 1
        assert session.current_emotional_state == EmotionalState.FRUSTRATED
        assert attempt in session.attempts


class TestPhilosophicalCommentary:
    """Test philosophical commentary generation."""
    
    def test_create_commentary(self):
        """Should create commentary object."""
        commentary = PhilosophicalCommentary(
            commentary_text="You tried. You failed.",
            attempt_trigger=5,
            emotional_context=EmotionalState.FRUSTRATED,
            is_mocking=True
        )
        
        assert "tried" in commentary.commentary_text
        assert commentary.is_mocking is True
    
    def test_generate_for_immediate_quit(self):
        """Should mock immediate quitters."""
        score = FrustrationScore(
            total_attempts=2,
            time_elapsed_seconds=10.0,
            max_rage_level=EmotionalState.CONFUSED,
            politeness_decay=5.0,
            profanity_creativity=0,
            caps_lock_escalation=0.0,
            plea_count=0,
            philosophical_score=10.0
        )
        
        commentary = PhilosophicalCommentary.generate_for_score(score)
        assert "gave up almost immediately" in commentary.lower()
        assert "impatient" in commentary.lower() or "understood" in commentary.lower()
    
    def test_generate_for_early_quit(self):
        """Should philosophize about early quitting."""
        score = FrustrationScore(
            total_attempts=7,
            time_elapsed_seconds=45.0,
            max_rage_level=EmotionalState.FRUSTRATED,
            politeness_decay=25.0,
            profanity_creativity=1,
            caps_lock_escalation=15.0,
            plea_count=1,
            philosophical_score=30.0
        )
        
        commentary = PhilosophicalCommentary.generate_for_score(score)
        assert "tried" in commentary.lower()
        assert "cowardice" in commentary.lower() or "admirable" in commentary.lower()
    
    def test_generate_for_moderate_persistence(self):
        """Should reflect on moderate persistence."""
        score = FrustrationScore(
            total_attempts=15,
            time_elapsed_seconds=120.0,
            max_rage_level=EmotionalState.ANGRY,
            politeness_decay=60.0,
            profanity_creativity=4,
            caps_lock_escalation=50.0,
            plea_count=3,
            philosophical_score=55.0
        )
        
        commentary = PhilosophicalCommentary.generate_for_score(score)
        assert "kept going" in commentary.lower() or "persisted" in commentary.lower()
        assert "never" in commentary.lower()
    
    def test_generate_for_high_persistence(self):
        """Should philosophize about stubbornness."""
        score = FrustrationScore(
            total_attempts=30,
            time_elapsed_seconds=300.0,
            max_rage_level=EmotionalState.ENRAGED,
            politeness_decay=85.0,
            profanity_creativity=8,
            caps_lock_escalation=80.0,
            plea_count=6,
            philosophical_score=75.0
        )
        
        commentary = PhilosophicalCommentary.generate_for_score(score)
        assert "stubbornness" in commentary.lower() or "obsession" in commentary.lower()
        assert "suffer" in commentary.lower()
    
    def test_generate_for_extreme_persistence(self):
        """Should respect extreme suffering."""
        score = FrustrationScore(
            total_attempts=60,
            time_elapsed_seconds=750.0,
            max_rage_level=EmotionalState.TRANSCENDENT,
            politeness_decay=100.0,
            profanity_creativity=15,
            caps_lock_escalation=95.0,
            plea_count=12,
            philosophical_score=90.0
        )
        
        commentary = PhilosophicalCommentary.generate_for_score(score)
        assert "patient" in commentary.lower() or "foolish" in commentary.lower()
        assert "lesson" in commentary.lower()
        assert "congratulations" in commentary.lower()
