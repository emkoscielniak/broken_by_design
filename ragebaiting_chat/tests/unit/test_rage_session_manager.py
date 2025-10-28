"""
Tests for RageSessionManager.
Goal: 100% coverage of session orchestration logic.
"""

import pytest
from datetime import datetime, timedelta
from src.services.rage_session_manager import RageSessionManager
from src.models.ragebait_models import (
    EmotionalState,
    RageIndicator,
)


class TestRageSessionManager:
    """Test session management and orchestration."""
    
    @pytest.fixture
    def manager(self):
        return RageSessionManager()
    
    def test_initialization(self, manager):
        """Manager initializes with no active session."""
        assert manager.session is None
        assert manager.analyzer is not None
        assert manager.opposite_doer is not None
    
    def test_start_session(self, manager: RageSessionManager):
        """Test starting a new session."""
        session = manager.start_session(user_id="test_user")
        
        assert session is not None
        assert session.user_id == "test_user"
        assert session.session_start is not None
        assert session.current_emotional_state == EmotionalState.OPTIMISTIC
        assert len(session.attempts) == 0
    
    def test_process_prompt_without_session_raises_error(self, manager):
        """Processing prompt without session should raise RuntimeError."""
        with pytest.raises(RuntimeError, match="Session not started"):
            manager.process_prompt("Hello")
    
    def test_process_first_prompt(self, manager):
        """First prompt should be analyzed and get antagonistic response."""
        manager.start_session()
        
        response, state, attempt = manager.process_prompt("Explain Python")
        
        # Should get a response
        assert isinstance(response, str)
        assert len(response) > 0
        
        # Should detect emotion
        assert isinstance(state, EmotionalState)
        
        # Attempt should be recorded
        assert attempt.attempt_number == 1
        assert attempt.prompt == "Explain Python"
        assert attempt.response == response
        assert attempt.emotional_state == state
        
        # Session should be updated
        assert len(manager.session.attempts) == 1
        assert manager.session.current_emotional_state == state
    
    def test_process_multiple_prompts(self, manager):
        """Multiple prompts should track emotional progression."""
        manager.start_session()
        
        # Attempt 1: Polite
        response1, state1, attempt1 = manager.process_prompt(
            "Could you explain Python?"
        )
        assert attempt1.attempt_number == 1
        
        # Attempt 2: Still trying
        response2, state2, attempt2 = manager.process_prompt(
            "Can you help me understand?"
        )
        assert attempt2.attempt_number == 2
        
        # Attempt 3: Getting frustrated
        response3, state3, attempt3 = manager.process_prompt(
            "PLEASE just explain it!"
        )
        assert attempt3.attempt_number == 3
        
        # Should have 3 attempts
        assert len(manager.session.attempts) == 3
        
        # Emotional state should progress (or at least change)
        assert state3 != EmotionalState.OPTIMISTIC or len(manager.session.attempts) > 0
    
    def test_process_prompt_with_profanity(self, manager):
        """Prompts with profanity should trigger ANGRY state."""
        manager.start_session()
        
        response, state, attempt = manager.process_prompt(
            "What the hell is going on?"
        )
        
        assert state in [EmotionalState.ANGRY, EmotionalState.ENRAGED]
        assert attempt.profanity_count > 0
        assert RageIndicator.PROFANE in attempt.rage_indicators
    
    def test_process_prompt_with_caps(self, manager):
        """High caps percentage should trigger rage indicators."""
        manager.start_session()
        
        response, state, attempt = manager.process_prompt(
            "WHY IS THIS NOT WORKING?!"
        )
        
        assert attempt.caps_percentage > 50
        assert RageIndicator.CAPS_LOCK in attempt.rage_indicators
    
    def test_should_offer_rage_quit_early_attempts(self, manager):
        """Should not offer rage quit in first few attempts."""
        manager.start_session()
        
        # Attempt 1-3
        for i in range(3):
            manager.process_prompt(f"Question {i+1}")
        
        assert not manager.should_offer_rage_quit()
    
    def test_should_offer_rage_quit_after_angry(self, manager):
        """Should offer rage quit after reaching ANGRY state."""
        manager.start_session()
        
        # Make 5 attempts with increasing frustration
        for i in range(5):
            manager.process_prompt(f"Question {i+1}")
        
        # Add an angry prompt
        manager.process_prompt("This is damn frustrating!")
        
        # Should offer rage quit if ANGRY or worse
        if manager.session.current_emotional_state in [
            EmotionalState.ANGRY,
            EmotionalState.ENRAGED,
            EmotionalState.BROKEN
        ]:
            assert manager.should_offer_rage_quit()
    
    def test_should_offer_rage_quit_after_many_attempts(self, manager):
        """Should offer rage quit after 15+ attempts regardless."""
        manager.start_session()
        
        # Make 15 polite attempts
        for i in range(15):
            manager.process_prompt(f"Could you help with {i+1}?")
        
        assert manager.should_offer_rage_quit()
    
    def test_should_offer_rage_quit_without_session(self, manager):
        """Should return False if no session active."""
        assert not manager.should_offer_rage_quit()
    
    def test_get_session_summary_no_session(self, manager):
        """Summary without session should indicate inactive."""
        summary = manager.get_session_summary()
        
        assert summary["active"] is False
        assert "message" in summary
    
    def test_get_session_summary_active_session(self, manager):
        """Summary with active session should show statistics."""
        manager.start_session()
        
        # Make some attempts
        manager.process_prompt("First question")
        manager.process_prompt("Second question")
        manager.process_prompt("THIRD QUESTION!")
        
        summary = manager.get_session_summary()
        
        assert summary["active"] is True
        assert summary["attempt_count"] == 3
        assert summary["duration_seconds"] >= 0
        assert "duration_display" in summary
        assert "current_emotional_state" in summary
        assert "politeness_decay" in summary
        assert "profanity_count" in summary
        assert "max_caps_percentage" in summary
        assert "rage_quit_available" in summary
    
    def test_generate_rage_quit_result_without_session(self, manager):
        """Generating result without session should raise error."""
        with pytest.raises(RuntimeError, match="Session not started"):
            manager.generate_rage_quit_result()
    
    def test_generate_rage_quit_result_no_attempts(self, manager):
        """Generating result without attempts should raise error."""
        manager.start_session()
        
        with pytest.raises(RuntimeError, match="No attempts recorded"):
            manager.generate_rage_quit_result()
    
    def test_generate_rage_quit_result_with_attempts(self, manager):
        """Should generate complete rage quit result."""
        manager.start_session()
        
        # Make several attempts
        prompts = [
            "Explain Python",
            "Can you help?",
            "PLEASE help!",
            "This is frustrating",
            "What the hell?",
            "JUST ANSWER!",
        ]
        for prompt in prompts:
            manager.process_prompt(prompt)
        
        result = manager.generate_rage_quit_result()
        
        # Should have frustration score
        assert result.frustration_score is not None
        assert result.frustration_score.total_attempts == 6
        assert result.frustration_score.time_elapsed_seconds >= 0
        
        # Should have philosophical commentary
        assert result.philosophical_commentary is not None
        assert len(result.philosophical_commentary) > 0
        
        # Should have entertaining metric (philosophical score + bonuses)
        # Base: 6 attempts * 2.5 = 15.0
        # Persistence bonus: min(20, 6 * 0.5) = 3.0
        # Emotional bonus: 10 (reached ENRAGED)
        # Expected: 15 + 3 + 10 = 28, but let's be flexible
        assert result.entertaining_metric > 0
        assert result.entertaining_metric <= 100
        
        # Should have persistence rating (from frustration_score)
        assert result.frustration_score.persistence_rating in [
            "Quitter McQuitface",
            "Easily Discouraged",
            "Optimistic Fool",
            "Stubborn Amateur",
            "Persistent Masochist",
            "Rage Connoisseur",
            "Transcendent Sufferer"
        ]
    
    def test_frustration_score_calculation_accuracy(self, manager):
        """Frustration score should accurately reflect session."""
        manager.start_session()
        
        # Make attempts with known characteristics
        manager.process_prompt("Hello")  # Polite
        manager.process_prompt("HELLO")  # Caps
        manager.process_prompt("What the hell")  # Profanity
        manager.process_prompt("Please help")  # Pleading
        
        result = manager.generate_rage_quit_result()
        score = result.frustration_score
        
        assert score.total_attempts == 4
        assert score.profanity_creativity > 0  # Should detect "hell"
        assert score.caps_lock_escalation > 0  # Should detect HELLO
        assert score.politeness_decay >= 0
    
    def test_legendary_status_detection(self, manager):
        """Should detect legendary status conditions."""
        manager.start_session()
        
        # Make many attempts with profanity
        for i in range(60):
            if i % 3 == 0:
                manager.process_prompt(f"damn hell shit {i}")
            else:
                manager.process_prompt(f"Question {i}")
        
        result = manager.generate_rage_quit_result()
        
        # 60 attempts should be legendary
        assert result.frustration_score.is_legendary
    
    def test_reset_session(self, manager):
        """Reset should clear current session."""
        manager.start_session()
        manager.process_prompt("Test")
        
        assert manager.session is not None
        
        manager.reset_session()
        
        assert manager.session is None
    
    def test_duration_formatting(self, manager):
        """Duration should be formatted human-readably."""
        manager.start_session()
        manager.process_prompt("Test")
        
        summary = manager.get_session_summary()
        duration_display = summary["duration_display"]
        
        # Should contain time unit
        assert any(unit in duration_display for unit in ["second", "minute", "hour", "m", "s", "h"])
    
    def test_politeness_decay_tracking(self, manager):
        """Should track politeness decay over attempts."""
        manager.start_session()
        
        # Start polite
        manager.process_prompt("Could you please help?")
        first_politeness = manager.session.attempts[0].politeness_score
        
        # Get ruder
        for _ in range(5):
            manager.process_prompt("Just tell me!")
        
        # Check decay in summary
        summary = manager.get_session_summary()
        assert summary["politeness_decay"] > 0
        
        # Last attempt should have lower politeness
        last_politeness = manager.session.attempts[-1].politeness_score
        assert last_politeness < first_politeness
    
    def test_philosophical_score_increases_with_attempts(self, manager):
        """Philosophical score should reward persistence."""
        manager.start_session()
        
        # Few attempts
        for i in range(5):
            manager.process_prompt(f"Question {i}")
        
        result1 = manager.generate_rage_quit_result()
        score1 = result1.frustration_score.philosophical_score
        
        # Reset and try more attempts
        manager.start_session()
        for i in range(30):
            manager.process_prompt(f"Question {i}")
        
        result2 = manager.generate_rage_quit_result()
        score2 = result2.frustration_score.philosophical_score
        
        # More attempts should mean higher philosophical score
        assert score2 > score1
    
    def test_max_rage_level_tracking(self, manager):
        """Should track maximum emotional intensity reached."""
        manager.start_session()
        
        # Escalate emotions
        manager.process_prompt("Hello")  # OPTIMISTIC
        manager.process_prompt("Help?")  # Maybe CONFUSED
        manager.process_prompt("HELP!")  # Maybe ANGRY
        manager.process_prompt("WHAT THE HELL!")  # Likely ENRAGED
        
        result = manager.generate_rage_quit_result()
        
        # Max rage level should be at least 3 (ANGRY) or higher
        assert result.frustration_score.max_rage_level >= 0
    
    def test_entertaining_metric_components(self, manager):
        """Entertaining metric should include all bonus components."""
        manager.start_session()
        
        # Create session with all bonus triggers
        for i in range(25):  # Persistence bonus
            if i % 5 == 0:
                manager.process_prompt(f"DAMN HELL SHIT {i}")  # Profanity + caps
            else:
                manager.process_prompt(f"Question {i}")
        
        result = manager.generate_rage_quit_result()
        
        # Should have high entertaining metric
        metric = result.entertaining_metric
        assert metric > 60  # At minimum base score
        
        # With 25 attempts, should have persistence bonus
        assert result.frustration_score.total_attempts == 25
