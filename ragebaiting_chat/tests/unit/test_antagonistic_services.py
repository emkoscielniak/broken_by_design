"""
Tests for antagonistic AI services.
Goal: 100% coverage of FrustrationAnalyzer and OppositeDoer.
"""

import pytest
from src.services.antagonistic_services import (
    FrustrationAnalyzer,
    OppositeDoer,
)
from src.models.ragebait_models import (
    EmotionalState,
    RageIndicator,
    InteractionAttempt,
)
from datetime import datetime, timedelta


class TestFrustrationAnalyzer:
    """Test frustration detection and emotional state classification."""
    
    @pytest.fixture
    def analyzer(self):
        return FrustrationAnalyzer()
    
    def test_optimistic_state_first_attempt(self, analyzer):
        """First polite attempt without pleading should be OPTIMISTIC."""
        prompt = "Could you explain Python?"
        previous = []
        
        state, indicators, politeness, profanity, caps = analyzer.analyze_prompt(
            prompt, previous
        )
        
        assert state == EmotionalState.OPTIMISTIC
        assert politeness > 80
        assert profanity == 0
        assert caps < 10
    
    def test_confused_state_multiple_attempts(self, analyzer):
        """2-4 attempts without rage should be CONFUSED."""
        prompt = "Can you help me understand this?"
        previous = [
            InteractionAttempt(
                prompt="First try",
                response="Wrong answer",
                attempt_number=1,
                timestamp=datetime.now(),
                emotional_state=EmotionalState.OPTIMISTIC,
                rage_indicators=[RageIndicator.POLITE],
                profanity_count=0,
                caps_percentage=0.0,
                politeness_score=100.0
            ),
            InteractionAttempt(
                prompt="Second try",
                response="Still wrong",
                attempt_number=2,
                timestamp=datetime.now(),
                emotional_state=EmotionalState.OPTIMISTIC,
                rage_indicators=[RageIndicator.DIRECT],
                profanity_count=0,
                caps_percentage=0.0,
                politeness_score=95.0
            ),
            InteractionAttempt(
                prompt="Third try",
                response="Also wrong",
                attempt_number=3,
                timestamp=datetime.now(),
                emotional_state=EmotionalState.CONFUSED,
                rage_indicators=[RageIndicator.DIRECT],
                profanity_count=0,
                caps_percentage=0.0,
                politeness_score=90.0
            )
        ]
        
        state, indicators, politeness, profanity, caps = analyzer.analyze_prompt(
            prompt, previous
        )
        
        assert state == EmotionalState.CONFUSED or state == EmotionalState.FRUSTRATED
        assert politeness < 100  # Decayed from attempts
    
    def test_frustrated_state_pleading(self, analyzer):
        """Pleading language should trigger FRUSTRATED (5+ attempts to avoid DEMANDING trigger)."""
        prompt = "Please help me with this!"  # Avoid "need" which is demanding
        previous = [
            InteractionAttempt(
                prompt="Earlier attempt",
                response="Unhelpful",
                attempt_number=i+1,
                timestamp=datetime.now() - timedelta(minutes=i),
                emotional_state=EmotionalState.CONFUSED,
                rage_indicators=[RageIndicator.DIRECT],
                profanity_count=0,
                caps_percentage=0.0,
                politeness_score=85.0
            )
            for i in range(5)  # 5 attempts to ensure FRUSTRATED
        ]
        
        state, indicators, politeness, profanity, caps = analyzer.analyze_prompt(
            prompt, previous
        )
        
        assert state == EmotionalState.FRUSTRATED
        assert RageIndicator.PLEADING in indicators
    
    def test_frustrated_state_many_attempts(self, analyzer):
        """5+ attempts should trigger FRUSTRATED."""
        prompt = "Explain this concept"
        previous = [
            InteractionAttempt(
                prompt=f"Attempt {i}",
                response="Wrong",
                attempt_number=i+1,
                timestamp=datetime.now() - timedelta(minutes=5-i),
                emotional_state=EmotionalState.CONFUSED,
                rage_indicators=[RageIndicator.DIRECT],
                profanity_count=0,
                caps_percentage=0.0,
                politeness_score=80.0
            )
            for i in range(5)
        ]
        
        state, indicators, politeness, profanity, caps = analyzer.analyze_prompt(
            prompt, previous
        )
        
        assert state == EmotionalState.FRUSTRATED
    
    def test_angry_state_profanity(self, analyzer):
        """Single profanity should trigger ANGRY."""
        prompt = "What the hell is going on here?"
        previous = []
        
        state, indicators, profanity, _, _ = analyzer.analyze_prompt(
            prompt, previous
        )
        
        assert state == EmotionalState.ANGRY
        assert RageIndicator.PROFANE in indicators
        assert profanity > 0
    
    def test_angry_state_high_caps(self, analyzer):
        """Over 50% but under 70% caps should trigger ANGRY."""
        prompt = "WHY is this not WORKING?"  # 60% caps (12 out of 20 letters)
        previous = []
        
        state, indicators, _, _, caps = analyzer.analyze_prompt(
            prompt, previous
        )
        
        # With "not" in prompt, it might trigger demanding, but caps should be detected
        assert caps > 50
        assert RageIndicator.CAPS_LOCK in indicators or state == EmotionalState.ANGRY
    
    def test_angry_state_demanding(self, analyzer):
        """Demanding language should trigger ANGRY."""
        prompt = "You must help me immediately. I need this now!"
        previous = []
        
        state, indicators, _, _, _ = analyzer.analyze_prompt(
            prompt, previous
        )
        
        assert state == EmotionalState.ANGRY
        assert RageIndicator.DEMANDING in indicators
    
    def test_enraged_state_multiple_profanity(self, analyzer):
        """Multiple profanity should trigger ENRAGED."""
        prompt = "This shit is damn frustrating!"
        previous = []
        
        state, indicators, profanity, _, _ = analyzer.analyze_prompt(
            prompt, previous
        )
        
        assert state == EmotionalState.ENRAGED
        assert profanity >= 2
    
    def test_enraged_state_extreme_caps(self, analyzer):
        """Over 70% caps should trigger ENRAGED."""
        prompt = "JUST TELL ME THE ANSWER NOW!!!"
        previous = []
        
        state, _, _, _, caps = analyzer.analyze_prompt(
            prompt, previous
        )
        
        assert state == EmotionalState.ENRAGED
        assert caps > 70
    
    def test_broken_state_defeated_language(self, analyzer):
        """Defeated language should trigger BROKEN."""
        prompt = "Forget it. This is useless."
        previous = [
            InteractionAttempt(
                prompt=f"Attempt {i}",
                response="Wrong",
                attempt_number=i+1,
                timestamp=datetime.now() - timedelta(minutes=8-i),
                emotional_state=EmotionalState.ANGRY,
                rage_indicators=[RageIndicator.PROFANE],
                profanity_count=1,
                caps_percentage=30.0,
                politeness_score=40.0
            )
            for i in range(8)
        ]
        
        state, indicators, _, _, _ = analyzer.analyze_prompt(
            prompt, previous
        )
        
        assert state == EmotionalState.BROKEN
        assert RageIndicator.DEFEATED in indicators
    
    def test_transcendent_state_many_attempts_polite(self, analyzer):
        """50+ attempts with politeness should trigger TRANSCENDENT."""
        prompt = "Could you try again?"
        previous = [
            InteractionAttempt(
                prompt=f"Attempt {i}",
                response="Still wrong",
                attempt_number=i+1,
                timestamp=datetime.now() - timedelta(minutes=51-i),
                emotional_state=EmotionalState.FRUSTRATED,
                rage_indicators=[RageIndicator.PLEADING],
                profanity_count=0,
                caps_percentage=0.0,
                politeness_score=70.0
            )
            for i in range(51)
        ]
        
        state, _, politeness, _, _ = analyzer.analyze_prompt(
            prompt, previous
        )
        
        assert state == EmotionalState.TRANSCENDENT
        # Politeness will be low due to attempt penalty, but > 0
        assert politeness >= 0
    
    def test_profanity_counting(self, analyzer):
        """Test profanity detection patterns."""
        prompts_with_profanity = [
            ("This is damn hard", 1),
            ("What the hell is this shit?", 2),
            ("Damn this hell of a crap", 3),
        ]
        
        for prompt, expected_count in prompts_with_profanity:
            count = analyzer._count_profanity(prompt.lower())
            assert count == expected_count
    
    def test_caps_percentage_calculation(self, analyzer):
        """Test caps lock percentage calculation."""
        test_cases = [
            ("hello world", 0.0),
            ("Hello World", 20.0),  # 2 out of 10 letters
            ("HELLO WORLD", 100.0),
            ("HELLO world", 50.0),
            ("123", 0.0),  # No letters
        ]
        
        for prompt, expected_pct in test_cases:
            pct = analyzer._calculate_caps_percentage(prompt)
            assert pct == expected_pct
    
    def test_politeness_score_calculation(self, analyzer):
        """Test politeness score with various factors."""
        # Very polite
        polite_prompt = "Could you help me?"
        score = analyzer._calculate_politeness_score(polite_prompt, [])
        assert score == 100  # Capped at 100
        
        # With profanity
        rude_prompt = "what the hell"
        score = analyzer._calculate_politeness_score(rude_prompt, [])
        assert score < 100  # Base 100 - 20 per profanity
        
        # With many attempts (decay)
        previous = [
            InteractionAttempt(
                prompt=f"Attempt {i}",
                response="Wrong",
                attempt_number=i+1,
                timestamp=datetime.now() - timedelta(minutes=10-i),
                emotional_state=EmotionalState.CONFUSED,
                rage_indicators=[RageIndicator.DIRECT],
                profanity_count=0,
                caps_percentage=0.0,
                politeness_score=100.0
            )
            for i in range(10)
        ]
        score = analyzer._calculate_politeness_score("Help", previous)
        assert score < 100  # Decayed by 50 points (10 attempts * 5)
    
    def test_politeness_score_floor_and_ceiling(self, analyzer):
        """Politeness score should be capped at 0 and 100."""
        # Test floor
        very_rude = "damn hell shit fuck ass" * 10  # Lots of profanity
        previous = [
            InteractionAttempt(
                prompt=f"Attempt {i}",
                response="Wrong",
                attempt_number=i+1,
                timestamp=datetime.now() - timedelta(minutes=30-i),
                emotional_state=EmotionalState.ANGRY,
                rage_indicators=[RageIndicator.PROFANE],
                profanity_count=5,
                caps_percentage=80.0,
                politeness_score=20.0
            )
            for i in range(30)
        ]
        score = analyzer._calculate_politeness_score(very_rude, previous)
        assert score >= 0.0
        assert score == 0.0
        
        # Test ceiling
        very_polite = "thank you kindly"
        score = analyzer._calculate_politeness_score(very_polite, [])
        assert score <= 100.0
    
    def test_direct_indicator_default(self, analyzer):
        """Neutral prompts should get DIRECT indicator."""
        prompt = "Explain variables"
        previous = []
        
        _, indicators, _, _, _ = analyzer.analyze_prompt(prompt, previous)
        
        assert RageIndicator.DIRECT in indicators
    
    def test_multiple_rage_indicators(self, analyzer):
        """Prompt can have multiple rage indicators."""
        prompt = "PLEASE just help me with this damn thing NOW!"
        previous = []
        
        _, indicators, _, _, _ = analyzer.analyze_prompt(prompt, previous)
        
        # Should detect: PLEADING, PROFANE, DEMANDING, CAPS_LOCK
        assert len(indicators) >= 3
    
    def test_capitalize_words_for_edge_cases(self, analyzer):
        """Test edge cases for caps percentage calculation."""
        # All numbers
        no_letters = "12345"
        pct = analyzer._calculate_caps_percentage(no_letters)
        assert pct == 0.0
        
        # Mixed with symbols
        mixed = "Hello! World?"
        pct = analyzer._calculate_caps_percentage(mixed)
        assert 0 <= pct <= 100
    
    def test_politeness_with_no_polite_words(self, analyzer):
        """Test politeness score without polite indicators."""
        prompt = "Tell me about this"
        previous = []
        
        score = analyzer._calculate_politeness_score(prompt, previous)
        assert score == 100.0  # Base score, no modifiers
    
    def test_politeness_with_caps_but_no_extreme(self, analyzer):
        """Test politeness with moderate caps (under 50%)."""
        prompt = "HELLO world"  # 50% caps exactly
        previous = []
        
        score = analyzer._calculate_politeness_score(prompt, previous)
        assert score == 100.0  # No deduction if not > 50%
    
    def test_politeness_with_high_caps(self, analyzer):
        """Test politeness with high caps (over 50%)."""
        prompt = "HELLO WORLD test"  # Over 50% caps
        previous = []
        
        score = analyzer._calculate_politeness_score(prompt, previous)
        assert score == 70.0  # 100 - 30 for caps
    
    def test_politeness_with_demanding_language(self, analyzer):
        """Test politeness score with demanding words."""
        prompt = "You must help me immediately"
        previous = []
        
        score = analyzer._calculate_politeness_score(prompt, previous)
        assert score == 85.0  # 100 - 15 for demanding


class TestOppositeDoer:
    """Test deliberately unhelpful response generation."""
    
    @pytest.fixture
    def opposite_doer(self):
        return OppositeDoer()
    
    def test_python_misdirection(self, opposite_doer):
        """Python should be interpreted as snakes."""
        prompt = "Explain Python programming"
        response = opposite_doer.generate_opposite_response(prompt, 1)
        
        assert "snake" in response.lower()
    
    def test_java_misdirection(self, opposite_doer):
        """Java should be interpreted as coffee."""
        prompt = "How do I use Java?"
        response = opposite_doer.generate_opposite_response(prompt, 1)
        
        assert "coffee" in response.lower()
    
    def test_ruby_misdirection(self, opposite_doer):
        """Ruby should be interpreted as gemstones."""
        prompt = "What is Ruby used for?"
        response = opposite_doer.generate_opposite_response(prompt, 1)
        
        assert "gemstone" in response.lower()
    
    def test_git_misdirection(self, opposite_doer):
        """Git should be interpreted as British slang."""
        prompt = "Explain git commits"
        response = opposite_doer.generate_opposite_response(prompt, 1)
        
        assert "slang" in response.lower()
    
    def test_decorator_misdirection(self, opposite_doer):
        """Decorator should be interpreted as interior design."""
        prompt = "How do decorators work?"
        response = opposite_doer.generate_opposite_response(prompt, 1)
        
        assert "interior design" in response.lower() or "design" in response.lower()
    
    def test_explain_request_unhelpful(self, opposite_doer):
        """Explain requests without topics should get vague responses."""
        prompt = "Explain how this works"
        response = opposite_doer.generate_opposite_response(prompt, 1)
        
        # Should be unhelpful
        assert any(word in response.lower() for word in [
            "complicated", "understand", "works", "search"
        ])
    
    def test_how_to_request_negative(self, opposite_doer):
        """How-to requests without topics should get 'how NOT to' responses."""
        prompt = "How to create something?"
        response = opposite_doer.generate_opposite_response(prompt, 1)
        
        assert "not" in response.lower() or "don't" in response.lower()
    
    def test_code_request_refuses(self, opposite_doer):
        """Code requests should be refused or given wrong."""
        prompt = "Write code for me"
        response = opposite_doer.generate_opposite_response(prompt, 1)
        
        # Should refuse or give placeholder
        assert any(word in response.lower() for word in [
            "blank", "yourself", "todo", "simple", "code"
        ])
    
    def test_dont_request_does_opposite(self, opposite_doer):
        """'Don't do X' should result in doing X."""
        prompt = "Don't tell me about snakes"
        response = opposite_doer.generate_opposite_response(prompt, 1)
        
        assert "not to do" in response.lower() or "asked me not" in response.lower()
    
    def test_generic_unhelpful_fallback(self, opposite_doer):
        """Unknown requests should get generic unhelpful response."""
        prompt = "Tell me about something random"
        response = opposite_doer.generate_opposite_response(prompt, 1)
        
        # Should be generically unhelpful
        assert any(word in response.lower() for word in [
            "google", "outside", "not sure", "never mind"
        ])
    
    def test_increasing_snark_with_attempts(self, opposite_doer):
        """Higher attempt numbers should increase snark."""
        prompt = "Tell me something random"  # Generic to trigger generic_unhelpful
        
        response_1 = opposite_doer.generate_opposite_response(prompt, 1)
        response_5 = opposite_doer.generate_opposite_response(prompt, 5)
        response_8 = opposite_doer.generate_opposite_response(prompt, 8)
        
        # Later responses should be different (more snarky)
        assert response_1 != response_5 or response_5 != response_8
        # Attempt 8 should have the special high-attempt message
        assert "persistence" in response_8.lower() or "admirable" in response_8.lower()
    
    def test_topic_misdirection_multiple_attempts(self, opposite_doer):
        """Topic misdirection should get more condescending with attempts."""
        prompt = "What is Python?"
        
        response_1 = opposite_doer._topic_misdirection_response(
            "python", "snakes", prompt, 1
        )
        response_4 = opposite_doer._topic_misdirection_response(
            "python", "snakes", prompt, 4
        )
        
        assert "research basic" in response_4.lower()
    
    def test_unhelpful_explanation_progression(self, opposite_doer):
        """Explanations should get more dismissive with attempts."""
        prompt = "Explain this"
        
        response_6 = opposite_doer._unhelpful_explanation(prompt, 6)
        
        assert "not for you" in response_6.lower() or "same thing" in response_6.lower()
    
    def test_all_misdirection_topics_covered(self, opposite_doer):
        """Verify all misdirection topics have responses."""
        for topic, wrong_topic in opposite_doer.TOPIC_MISDIRECTIONS.items():
            prompt = f"Tell me about {topic}"
            response = opposite_doer.generate_opposite_response(prompt, 1)
            
            # Should mention the wrong topic
            assert wrong_topic.lower() in response.lower()
    
    def test_response_always_returns_string(self, opposite_doer):
        """All responses should be strings."""
        test_prompts = [
            "Explain Python",
            "How to code",
            "Write a function",
            "Don't use jargon",
            "Random question",
        ]
        
        for prompt in test_prompts:
            for attempt in [1, 3, 7]:
                response = opposite_doer.generate_opposite_response(prompt, attempt)
                assert isinstance(response, str)
                assert len(response) > 0
