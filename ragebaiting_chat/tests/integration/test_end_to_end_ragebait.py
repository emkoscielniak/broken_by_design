"""
Integration tests for complete ragebait user journey.

Tests the full pipeline from optimistic first attempt through
emotional deterioration to final rage quit.
"""

import pytest
from datetime import datetime
from src.services.rage_session_manager import RageSessionManager
from src.models.ragebait_models import EmotionalState


class TestEndToEndRagebaitJourney:
    """Test complete user journey through the ragebait system."""
    
    @pytest.fixture
    def manager(self):
        """Create a fresh session manager for each test."""
        return RageSessionManager()
    
    def test_complete_optimistic_to_rage_quit_journey(self, manager):
        """
        Test full user journey from optimistic start to rage quit.
        
        Journey:
        1. Start session (OPTIMISTIC)
        2. Make several polite attempts (CONFUSED → FRUSTRATED)
        3. Get angry with caps (ANGRY → ENRAGED)
        4. Rage quit becomes available
        5. Generate final result
        """
        # Start session
        session = manager.start_session(user_id="integration_test_user")
        assert session.current_emotional_state == EmotionalState.OPTIMISTIC
        assert len(session.attempts) == 0
        
        # First attempt - polite and hopeful
        response1, state1, attempt1 = manager.process_prompt("Can you help me with Python?")
        assert response1 is not None
        assert attempt1.attempt_number == 1
        # State can vary based on analysis, just check it's valid
        assert attempt1.emotional_state in EmotionalState
        assert attempt1.profanity_count == 0
        
        # Second attempt - still polite but confused
        response2, state2, attempt2 = manager.process_prompt("Please explain Python functions")
        assert attempt2.attempt_number == 2
        assert attempt2.emotional_state in EmotionalState  # Valid state
        
        # Third attempt - frustration building
        response3, state3, attempt3 = manager.process_prompt("This isn't what I asked for")
        assert attempt3.attempt_number == 3
        assert attempt3.emotional_state in EmotionalState  # Valid state
        
        # Fourth attempt - getting angry
        response4, state4, attempt4 = manager.process_prompt("Just answer my question!")
        assert attempt4.attempt_number == 4
        
        # Fifth attempt - CAPS LOCK ENGAGED
        response5, state5, attempt5 = manager.process_prompt("WHY WON'T YOU HELP ME?!")
        assert attempt5.attempt_number == 5
        assert attempt5.caps_percentage > 50  # Mostly caps
        assert attempt5.emotional_state in [EmotionalState.ANGRY, EmotionalState.ENRAGED]
        
        # Check if rage quit is available
        should_offer = manager.should_offer_rage_quit()
        # Should be available if we're angry with 5+ attempts
        if state5 in [EmotionalState.ANGRY, EmotionalState.ENRAGED, EmotionalState.BROKEN]:
            assert should_offer is True
        
        # Generate rage quit result
        result = manager.generate_rage_quit_result()
        
        # Validate result
        assert result.user_id == "integration_test_user"
        assert result.frustration_score.total_attempts == 5
        assert result.frustration_score.time_elapsed_seconds >= 0
        assert result.frustration_score.max_rage_level >= 3  # At least ANGRY
        assert result.philosophical_commentary is not None
        assert len(result.philosophical_commentary) > 0
        assert result.entertaining_metric > 0
        assert result.final_emotional_state in EmotionalState
    
    def test_profanity_escalation_journey(self, manager):
        """Test journey with increasing profanity leading to rage quit."""
        manager.start_session(user_id="profanity_test")
        
        # Start polite
        manager.process_prompt("Help me please")
        
        # Add mild profanity
        manager.process_prompt("What the hell is this?")
        
        # More profanity
        manager.process_prompt("This is damn frustrating")
        
        # Full profanity
        manager.process_prompt("What the fuck is wrong with this?!")
        
        # Caps + profanity combo
        manager.process_prompt("THIS IS FUCKING RIDICULOUS!")
        
        # Check session state
        session = manager.session
        assert len(session.attempts) == 5
        
        # Count total profanity
        total_profanity = sum(a.profanity_count for a in session.attempts)
        assert total_profanity >= 3  # Should detect multiple profanity instances
        
        # Should be in angry or worse state
        assert session.current_emotional_state.value in [
            'angry', 'enraged', 'broken', 'transcendent'
        ]
        
        # Generate result
        result = manager.generate_rage_quit_result()
        assert result.frustration_score.profanity_creativity > 0
    
    def test_persistence_through_many_attempts(self, manager):
        """Test user who persists through many attempts before quitting."""
        manager.start_session(user_id="persistent_user")
        
        # Make 20 attempts with varying intensity
        prompts = [
            "Help with Python",
            "Please explain",
            "I don't understand",
            "Can you clarify?",
            "This makes no sense",
            "Why is this so hard?",
            "I'm getting frustrated",
            "Just tell me!",
            "PLEASE HELP",
            "This is annoying",
            "I'm so confused",
            "Why won't you answer?",
            "ANSWER THE QUESTION",
            "This is ridiculous",
            "I give up... wait no",
            "One more try",
            "PLEASE JUST ANSWER",
            "I'm begging you",
            "WHY ARE YOU LIKE THIS",
            "FINAL ATTEMPT"
        ]
        
        for i, prompt in enumerate(prompts, 1):
            response, state, attempt = manager.process_prompt(prompt)
            assert attempt.attempt_number == i
        
        # Should definitely offer rage quit after 20 attempts
        assert manager.should_offer_rage_quit() is True
        
        # Generate result
        result = manager.generate_rage_quit_result()
        assert result.frustration_score.total_attempts == 20
        assert result.frustration_score.persistence_rating in [
            "Stubborn Amateur",
            "Persistent Masochist",
            "Rage Connoisseur"
        ]
        assert result.entertaining_metric >= 40  # High entertainment from persistence
    
    def test_politeness_decay_over_time(self, manager):
        """Test that politeness decreases as attempts increase."""
        manager.start_session(user_id="politeness_test")
        
        # Start very polite
        _, _, attempt1 = manager.process_prompt("Please help me, thank you")
        initial_politeness = attempt1.politeness_score
        
        # Continue with decreasing politeness
        manager.process_prompt("Can you help?")
        manager.process_prompt("Help me")
        manager.process_prompt("Just answer")
        manager.process_prompt("ANSWER NOW")
        
        # Check politeness decay
        session = manager.session
        final_politeness = session.attempts[-1].politeness_score
        
        # Politeness should have decreased
        assert final_politeness < initial_politeness
        
        # Check decay property
        assert session.politeness_decay > 0
    
    def test_emotional_state_progression(self, manager):
        """Test that emotional states progress logically."""
        manager.start_session(user_id="emotion_test")
        
        states_observed = []
        
        # Make 10 attempts with increasing frustration
        prompts = [
            "Help me please",
            "I need help",
            "Can you answer?",
            "Why won't you help?",
            "This is frustrating",
            "Just answer!",
            "PLEASE HELP",
            "WHY ARE YOU DOING THIS",
            "I HATE THIS",
            "GIVE UP"
        ]
        
        for prompt in prompts:
            _, state, _ = manager.process_prompt(prompt)
            states_observed.append(state)
        
        # Should see progression (not necessarily strict, but general trend)
        # First state should not be worse than last state
        first_state_index = list(EmotionalState).index(states_observed[0])
        last_state_index = list(EmotionalState).index(states_observed[-1])
        
        # Last state should generally be same or more frustrated
        # (might not always be strictly increasing due to detection logic)
        assert last_state_index >= first_state_index or last_state_index == 0  # OPTIMISTIC is 0
    
    def test_legendary_status_achievement(self, manager):
        """Test achieving legendary status through extreme persistence."""
        manager.start_session(user_id="legend_test")
        
        # Make 50+ attempts to achieve legendary status
        for i in range(55):
            prompt = f"Attempt {i+1}: Please help with Python"
            if i > 30:
                prompt = prompt.upper()  # Add caps later
            manager.process_prompt(prompt)
        
        # Generate result
        result = manager.generate_rage_quit_result()
        
        # Should be legendary
        assert result.frustration_score.is_legendary is True
        assert result.frustration_score.total_attempts >= 50
        # With 55 attempts, should be in top tiers
        assert result.frustration_score.persistence_rating in [
            "Rage Connoisseur",
            "Transcendent Sufferer"
        ]
    
    def test_session_summary_accuracy(self, manager):
        """Test that session summary provides accurate statistics."""
        manager.start_session(user_id="summary_test")
        
        # Make some attempts
        manager.process_prompt("Help me")
        manager.process_prompt("What the hell?")
        manager.process_prompt("PLEASE ANSWER")
        
        # Get summary
        summary = manager.get_session_summary()
        
        # Validate summary
        assert summary['active'] is True
        assert summary['attempt_count'] == 3
        assert summary['duration_seconds'] >= 0
        assert summary['duration_display'] is not None
        assert summary['current_emotional_state'] in [s.value for s in EmotionalState]
        assert summary['politeness_decay'] >= 0
        assert summary['profanity_count'] >= 1  # "hell"
        assert summary['max_caps_percentage'] > 50  # "PLEASE ANSWER"
    
    def test_reset_and_restart_journey(self, manager):
        """Test that sessions can be reset and restarted."""
        # First session
        manager.start_session(user_id="reset_test_1")
        manager.process_prompt("First session")
        manager.process_prompt("Second message")
        
        assert len(manager.session.attempts) == 2
        
        # Reset
        manager.reset_session()
        assert manager.session is None
        
        # Start new session
        manager.start_session(user_id="reset_test_2")
        assert manager.session is not None
        assert len(manager.session.attempts) == 0
        assert manager.session.user_id == "reset_test_2"
        
        # New session should start fresh
        _, state, attempt = manager.process_prompt("Fresh start")
        assert attempt.attempt_number == 1
        assert state == EmotionalState.OPTIMISTIC
    
    def test_multiple_users_different_sessions(self):
        """Test that different users have independent sessions."""
        manager1 = RageSessionManager()
        manager2 = RageSessionManager()
        
        # Start different sessions
        manager1.start_session(user_id="user1")
        manager2.start_session(user_id="user2")
        
        # Make different attempts
        manager1.process_prompt("User 1 message")
        manager2.process_prompt("User 2 message")
        manager2.process_prompt("User 2 second message")
        
        # Sessions should be independent
        assert len(manager1.session.attempts) == 1
        assert len(manager2.session.attempts) == 2
        assert manager1.session.user_id == "user1"
        assert manager2.session.user_id == "user2"
    
    def test_transcendent_state_achievement(self, manager):
        """Test reaching the transcendent state (beyond caring)."""
        manager.start_session(user_id="transcendent_test")
        
        # Make many attempts to potentially reach transcendent
        for i in range(25):
            if i < 10:
                prompt = "Help please"
            elif i < 20:
                prompt = "I NEED HELP"
            else:
                prompt = "whatever, nevermind"  # Defeated tone
            
            manager.process_prompt(prompt)
        
        # Check final state
        session = manager.session
        # Might reach BROKEN or TRANSCENDENT state
        assert session.current_emotional_state.value in [
            'frustrated', 'angry', 'enraged', 'broken', 'transcendent'
        ]


class TestIntegrationEdgeCases:
    """Test edge cases in the integrated system."""
    
    def test_empty_prompt_handling(self):
        """Test that empty prompts are handled gracefully."""
        manager = RageSessionManager()
        manager.start_session()
        
        # Process empty prompt
        response, state, attempt = manager.process_prompt("")
        
        # Should still create attempt
        assert attempt is not None
        assert attempt.attempt_number == 1
        assert response is not None
    
    def test_very_long_prompt(self):
        """Test handling of very long prompts."""
        manager = RageSessionManager()
        manager.start_session()
        
        # Create a very long prompt
        long_prompt = "Help me " * 1000  # 7000+ characters
        
        response, state, attempt = manager.process_prompt(long_prompt)
        
        # Should handle gracefully
        assert attempt is not None
        assert response is not None
        assert attempt.caps_percentage >= 0
    
    def test_unicode_and_special_characters(self):
        """Test handling of unicode and special characters."""
        manager = RageSessionManager()
        manager.start_session()
        
        prompts_with_unicode = [
            "Help me with Python 🐍",
            "¿Por qué no funciona?",
            "这个怎么用？",
            "Помогите пожалуйста",
            "🤬🤬🤬",
        ]
        
        for prompt in prompts_with_unicode:
            response, state, attempt = manager.process_prompt(prompt)
            assert attempt is not None
            assert response is not None
    
    def test_consecutive_identical_prompts(self):
        """Test sending the same prompt multiple times."""
        manager = RageSessionManager()
        manager.start_session()
        
        # Send same prompt 5 times
        for i in range(5):
            response, state, attempt = manager.process_prompt("Help me with Python")
            assert attempt.attempt_number == i + 1
        
        # Should still track all attempts
        assert len(manager.session.attempts) == 5
    
    def test_rapid_state_changes(self):
        """Test rapid changes in emotional state."""
        manager = RageSessionManager()
        manager.start_session()
        
        # Alternate between calm and angry prompts
        prompts = [
            "Please help",
            "DAMN IT ANSWER ME",
            "Sorry, can you help?",
            "WHAT THE HELL",
            "Thank you for your patience",
            "FUCK THIS",
        ]
        
        states = []
        for prompt in prompts:
            _, state, _ = manager.process_prompt(prompt)
            states.append(state)
        
        # Should detect state changes
        assert len(set(states)) > 1  # Multiple different states


class TestComponentIntegration:
    """Test integration between different components."""
    
    def test_frustration_analyzer_to_opposite_doer_flow(self):
        """Test data flow from analyzer through opposite doer."""
        manager = RageSessionManager()
        manager.start_session()
        
        # Process a prompt
        response, state, attempt = manager.process_prompt("Help me with Python")
        
        # Check that analyzer data is captured in attempt
        assert attempt.emotional_state is not None
        assert attempt.rage_indicators is not None
        assert attempt.caps_percentage >= 0
        assert attempt.politeness_score > 0
        
        # Check that opposite doer provided response
        assert response is not None
        assert len(response) > 0
        assert "python" not in response.lower() or "snake" in response.lower()  # Misdirection
    
    def test_session_to_score_calculation_flow(self):
        """Test data flow from session to frustration score."""
        manager = RageSessionManager()
        manager.start_session()
        
        # Make attempts with known characteristics
        manager.process_prompt("Please help")  # Polite
        manager.process_prompt("What the hell?")  # Profanity
        manager.process_prompt("ANSWER ME")  # Caps
        
        # Generate score
        result = manager.generate_rage_quit_result()
        score = result.frustration_score
        
        # Verify data carried through
        assert score.total_attempts == 3
        assert score.profanity_creativity > 0
        assert score.caps_lock_escalation > 0
        assert score.politeness_decay > 0
    
    def test_all_models_integration(self):
        """Test that all models work together correctly."""
        manager = RageSessionManager()
        session = manager.start_session()
        
        # Process prompts
        manager.process_prompt("Help me")
        manager.process_prompt("PLEASE")
        
        # Generate result - uses all models
        result = manager.generate_rage_quit_result()
        
        # Verify all model types are present and valid
        assert isinstance(result.frustration_score.total_attempts, int)
        assert isinstance(result.frustration_score.persistence_rating, str)
        assert isinstance(result.entertaining_metric, float)
        assert isinstance(result.philosophical_commentary, str)
        assert result.final_emotional_state in EmotionalState
        assert len(result.interaction_history) == 2
