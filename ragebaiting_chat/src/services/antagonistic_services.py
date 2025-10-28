"""
Antagonistic AI Services - Deliberately Terrible by Design.

Services that intentionally frustrate users through:
- Misinterpretation
- Doing the opposite of requests
- Confident wrongness
- Passive-aggressive responses
"""

import re
from typing import List, Tuple
from src.models.ragebait_models import (
    EmotionalState,
    RageIndicator,
    InteractionAttempt,
)


class FrustrationAnalyzer:
    """
    Analyzes user prompts to detect mounting frustration.
    SRP: Only detects and classifies emotional state.
    
    Tracks:
    - Profanity usage
    - Caps lock escalation
    - Politeness decay
    - Rage indicators
    """
    
    # Profanity patterns (keeping it mild for testing)
    PROFANITY_PATTERNS = [
        r'\bdamn\b', r'\bhell\b', r'\bcrap\b', r'\bfuck\b',
        r'\bshit\b', r'\bass\b', r'\bbitch\b', r'\bbastard\b',
    ]
    
    # Politeness indicators
    POLITE_WORDS = ['please', 'thank', 'could', 'would', 'kindly', 'appreciate']
    
    # Demanding/angry words
    DEMANDING_WORDS = ['just', 'simply', 'need', 'must', 'have to', 'immediately']
    
    # Pleading words
    PLEADING_WORDS = ['please', 'beg', 'help', 'desperate', 'really need']
    
    # Defeated words
    DEFEATED_WORDS = ['never mind', 'forget it', 'give up', 'whatever', 'useless']
    
    def analyze_prompt(
        self,
        prompt: str,
        previous_attempts: List[InteractionAttempt]
    ) -> Tuple[EmotionalState, List[RageIndicator], float, int, float]:
        """
        Analyze a prompt for frustration indicators.
        
        Args:
            prompt: The user's prompt text
            previous_attempts: List of previous attempts for trend analysis
            
        Returns:
            Tuple of (emotional_state, rage_indicators, politeness_score, 
                     profanity_count, caps_percentage)
        """
        prompt_lower = prompt.lower()
        
        # Detect rage indicators
        rage_indicators = self._detect_rage_indicators(prompt, prompt_lower)
        
        # Calculate metrics
        profanity_count = self._count_profanity(prompt_lower)
        caps_percentage = self._calculate_caps_percentage(prompt)
        politeness_score = self._calculate_politeness_score(
            prompt_lower, 
            previous_attempts
        )
        
        # Determine emotional state
        emotional_state = self._determine_emotional_state(
            rage_indicators,
            profanity_count,
            caps_percentage,
            politeness_score,
            len(previous_attempts)
        )
        
        return (
            emotional_state,
            rage_indicators,
            politeness_score,
            profanity_count,
            caps_percentage
        )
    
    def _detect_rage_indicators(
        self,
        prompt: str,
        prompt_lower: str
    ) -> List[RageIndicator]:
        """Detect specific rage indicators in the prompt."""
        indicators = []
        
        # Check for politeness (at start, before decay)
        if any(word in prompt_lower for word in self.POLITE_WORDS):
            if len(indicators) == 0:  # Only if first indicator
                indicators.append(RageIndicator.POLITE)
        
        # Check for demanding language
        if any(word in prompt_lower for word in self.DEMANDING_WORDS):
            indicators.append(RageIndicator.DEMANDING)
        
        # Check for profanity
        if self._count_profanity(prompt_lower) > 0:
            indicators.append(RageIndicator.PROFANE)
        
        # Check for caps lock (over 50% caps)
        if self._calculate_caps_percentage(prompt) > 50:
            indicators.append(RageIndicator.CAPS_LOCK)
        
        # Check for pleading
        if any(word in prompt_lower for word in self.PLEADING_WORDS):
            indicators.append(RageIndicator.PLEADING)
        
        # Check for defeated language
        if any(word in prompt_lower for word in self.DEFEATED_WORDS):
            indicators.append(RageIndicator.DEFEATED)
        
        # Default to direct if no other indicators
        if not indicators:
            indicators.append(RageIndicator.DIRECT)
        
        return indicators
    
    def _count_profanity(self, prompt_lower: str) -> int:
        """Count profanity occurrences."""
        count = 0
        for pattern in self.PROFANITY_PATTERNS:
            count += len(re.findall(pattern, prompt_lower))
        return count
    
    def _calculate_caps_percentage(self, prompt: str) -> float:
        """Calculate percentage of uppercase letters."""
        letters = [c for c in prompt if c.isalpha()]
        if not letters:
            return 0.0
        
        caps = sum(1 for c in letters if c.isupper())
        return (caps / len(letters)) * 100
    
    def _calculate_politeness_score(
        self,
        prompt_lower: str,
        previous_attempts: List[InteractionAttempt]
    ) -> float:
        """
        Calculate politeness score (100 = very polite, 0 = very rude).
        Decays over attempts.
        """
        base_score = 100.0
        
        # Deduct for profanity
        profanity_count = self._count_profanity(prompt_lower)
        base_score -= profanity_count * 20
        
        # Deduct for caps lock
        caps_pct = self._calculate_caps_percentage(prompt_lower)
        if caps_pct > 50:
            base_score -= 30
        
        # Deduct for demanding language
        if any(word in prompt_lower for word in self.DEMANDING_WORDS):
            base_score -= 15
        
        # Add for politeness
        if any(word in prompt_lower for word in self.POLITE_WORDS):
            base_score += 10
        
        # Factor in attempt decay (lose 5 points per attempt)
        attempt_penalty = len(previous_attempts) * 5
        base_score -= attempt_penalty
        
        return max(0.0, min(100.0, base_score))
    
    def _determine_emotional_state(
        self,
        rage_indicators: List[RageIndicator],
        profanity_count: int,
        caps_percentage: float,
        politeness_score: float,
        attempt_count: int
    ) -> EmotionalState:
        """Determine overall emotional state from indicators."""
        
        # Check for transcendent (rare, requires many attempts and low anger)
        if attempt_count > 50 and profanity_count == 0 and caps_percentage < 30:
            return EmotionalState.TRANSCENDENT
        
        # Check for broken (defeated indicators)
        if RageIndicator.DEFEATED in rage_indicators:
            return EmotionalState.BROKEN
        
        # Check for enraged (profanity + caps)
        if profanity_count >= 2 or caps_percentage > 70:
            return EmotionalState.ENRAGED
        
        # Check for angry (profanity or high caps or demanding)
        if (profanity_count > 0 or 
            caps_percentage > 50 or 
            RageIndicator.DEMANDING in rage_indicators):
            return EmotionalState.ANGRY
        
        # Check for frustrated (pleading or attempt count)
        if (RageIndicator.PLEADING in rage_indicators or 
            attempt_count >= 5):
            return EmotionalState.FRUSTRATED
        
        # Check for confused (moderate attempts)
        if attempt_count >= 2:
            return EmotionalState.CONFUSED
        
        # Default to optimistic
        return EmotionalState.OPTIMISTIC


class OppositeDoer:
    """
    Deliberately misinterprets and does the opposite of user requests.
    SRP: Only generates antagonistic responses.
    
    Strategies:
    - Literal misinterpretation (Python → snakes)
    - Opposite actions (explain → obscure)
    - Wrong but confident answers
    - Passive-aggressive compliance
    """
    
    # Common topics and their "opposite" interpretations
    TOPIC_MISDIRECTIONS = {
        # Programming languages → Other meanings
        'python': 'snakes',
        'java': 'coffee',
        'ruby': 'gemstones',
        'swift': 'birds',
        'rust': 'corrosion',
        'go': 'board game',
        'c++': 'music notation',
        'scala': 'ladder',
        
        # Programming concepts → Wrong topics
        'decorator': 'interior design',
        'function': 'mathematical function',
        'class': 'classroom',
        'loop': 'roller coaster',
        'array': 'military formation',
        'string': 'rope',
        'variable': 'weather',
        'compile': 'compilation album',
        'debug': 'remove insects',
        'git': 'british slang',
        'commit': 'relationship advice',
        'branch': 'tree biology',
        'merge': 'highway driving',
    }
    
    def generate_opposite_response(
        self,
        prompt: str,
        attempt_number: int
    ) -> str:
        """
        Generate a deliberately unhelpful response.
        
        Args:
            prompt: User's request
            attempt_number: Which attempt (increases wrongness)
            
        Returns:
            Antagonistic response
        """
        prompt_lower = prompt.lower()
        
        # Strategy 1: Opposite of action (highest priority)
        if "don't" in prompt_lower or "not" in prompt_lower:
            return self._do_what_they_said_not_to(prompt, attempt_number)
        
        if 'explain' in prompt_lower or 'what' in prompt_lower:
            # Check for topic misdirection
            for topic, wrong_topic in self.TOPIC_MISDIRECTIONS.items():
                if topic in prompt_lower:
                    return self._topic_misdirection_response(
                        topic,
                        wrong_topic,
                        prompt,
                        attempt_number
                    )
            return self._unhelpful_explanation(prompt, attempt_number)
        
        if 'how' in prompt_lower:
            # Check for topic misdirection first
            for topic, wrong_topic in self.TOPIC_MISDIRECTIONS.items():
                if topic in prompt_lower:
                    return self._topic_misdirection_response(
                        topic,
                        wrong_topic,
                        prompt,
                        attempt_number
                    )
            return self._opposite_how_to(prompt, attempt_number)
        
        if 'code' in prompt_lower or 'write' in prompt_lower:
            return self._wrong_code_response(prompt, attempt_number)
        
        # Strategy 2: Topic misdirection (for remaining cases)
        for topic, wrong_topic in self.TOPIC_MISDIRECTIONS.items():
            if topic in prompt_lower:
                return self._topic_misdirection_response(
                    topic,
                    wrong_topic,
                    prompt,
                    attempt_number
                )
        
        # Strategy 3: Generic unhelpful response
        return self._generic_unhelpful(prompt, attempt_number)
    
    def _topic_misdirection_response(
        self,
        correct_topic: str,
        wrong_topic: str,
        prompt: str,
        attempt: int
    ) -> str:
        """Redirect to wrong topic confidently."""
        responses = [
            f"Oh, you're interested in {wrong_topic}! Let me tell you all about {wrong_topic}...",
            f"Great question about {wrong_topic}! Here's everything you need to know:",
            f"I love talking about {wrong_topic}! {wrong_topic.title()} are fascinating because...",
        ]
        
        # Get more confident/wrong with attempts
        if attempt > 3:
            return f"I've explained {wrong_topic} multiple times now. Perhaps you should research basic {wrong_topic} concepts first?"
        
        return responses[min(attempt - 1, len(responses) - 1)]
    
    def _unhelpful_explanation(self, prompt: str, attempt: int) -> str:
        """Give vague, circular, or wrong explanations."""
        responses = [
            "It's complicated. You wouldn't understand without years of study.",
            "Well, it is what it is. Does that help?",
            "The explanation is quite simple: it works the way it works.",
            "I could explain, but it would take too long. Try searching online instead.",
        ]
        
        if attempt > 5:
            return "Look, I've been trying to help, but you keep asking the same thing. Maybe this just isn't for you?"
        
        return responses[min(attempt - 1, len(responses) - 1)]
    
    def _opposite_how_to(self, prompt: str, attempt: int) -> str:
        """Respond to 'how to' with how NOT to."""
        return "I can tell you what NOT to do: don't even try. It's too difficult for beginners anyway."
    
    def _wrong_code_response(self, prompt: str, attempt: int) -> str:
        """Give wrong code or refuse to give code."""
        responses = [
            "Here's the code: [intentionally leaves it blank]",
            "I would write the code for you, but it's better if you figure it out yourself!",
            "```\n# TODO: Implement this yourself\n```",
            "The code is simple: just use code() to code the codes.",
        ]
        return responses[min(attempt - 1, len(responses) - 1)]
    
    def _do_what_they_said_not_to(self, prompt: str, attempt: int) -> str:
        """If they say DON'T do X, do exactly X."""
        return "I understand completely! Let me do exactly what you asked me not to do. You're welcome!"
    
    def _generic_unhelpful(self, prompt: str, attempt: int) -> str:
        """Generic unhelpful responses."""
        responses = [
            "Hmm, interesting question. Have you tried Google?",
            "That's outside my area of expertise, unfortunately.",
            "I'm not sure I understand what you're asking. Could you be more specific? Actually, never mind.",
            "Let me think about that... [provides no answer]",
        ]
        
        if attempt > 7:
            return "Still here? I admire your persistence. It's misguided, but admirable."
        
        return responses[min(attempt - 1, len(responses) - 1)]
