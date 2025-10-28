"""
God Object - Violating SOLID Principles By Design

This module deliberately violates EVERY SOLID principle:
- Single Responsibility: Does EVERYTHING in one class
- Open/Closed: Hard to extend without modifying
- Liskov Substitution: No inheritance, just one massive class
- Interface Segregation: One massive interface
- Dependency Inversion: Depends on concrete implementations

This is intentionally terrible code that somehow still works.
"""

import re
import random
from datetime import datetime
from typing import List, Optional, Tuple


class GodObject:
    """
    The ultimate anti-pattern: A God Object that does EVERYTHING.
    
    Violates:
    - SRP: Handles analysis, generation, session management, scoring, etc.
    - OCP: Hard-coded logic everywhere, difficult to extend
    - LSP: No inheritance hierarchy
    - ISP: Clients forced to depend on methods they don't use
    - DIP: Depends on concrete implementations, no abstractions
    """
    
    def __init__(self):
        """Initialize with hardcoded dependencies."""
        # Violation: Everything in one place
        self.user_id = None
        self.session_start = None
        self.attempts = []
        self.current_state = "optimistic"
        
        # Violation: Hardcoded magic numbers
        self.profanity_words = ["fuck", "shit", "damn", "hell", "ass", "bitch", "crap"]
        self.polite_words = ["please", "thank", "kindly", "appreciate", "sorry"]
        
        # Violation: Hardcoded misdirection topics
        self.misdirections = {
            "python": "snakes",
            "java": "coffee",
            "javascript": "a scripting language for making web pages blink",
            "git": "a British slang term",
            "react": "a chemical process",
            "node": "a point where lines intersect",
            "database": "a place where you store bases",
            "api": "a type of monkey (wait, that's ape)",
            "docker": "someone who works at a shipping yard",
            "kubernetes": "a Greek shipping term",
        }
        
        # Violation: Hardcoded responses
        self.sarcastic_responses = [
            "Oh, that's fascinating. Let me tell you about something completely unrelated...",
            "I could answer that, but let me tell you about {topic} instead!",
            "That's outside my area of expertise, unfortunately.",
            "Have you considered that maybe you're asking the wrong question?",
            "I'm not sure I understand what you're asking. Could you be more specific? Actually, never mind.",
            "Let me think about that... [provides no answer]",
            "That's a great question! Too bad I'm going to answer a different one.",
        ]
    
    def do_everything(self, user_input: str) -> dict:
        """
        The mother of all methods: Does EVERYTHING.
        
        Violation: Single method with 100+ lines handling multiple responsibilities.
        """
        # Step 1: Analyze frustration (should be separate class)
        caps_count = sum(1 for c in user_input if c.isupper())
        total_chars = len(user_input)
        caps_percentage = (caps_count / total_chars * 100) if total_chars > 0 else 0
        
        profanity_count = 0
        for word in self.profanity_words:
            profanity_count += user_input.lower().count(word)
        
        politeness_score = 100.0
        for word in self.polite_words:
            if word in user_input.lower():
                politeness_score += 10
        politeness_score = min(politeness_score, 100)
        
        # Step 2: Determine emotional state (should be separate strategy)
        if profanity_count >= 3 or caps_percentage > 80:
            emotional_state = "enraged"
        elif profanity_count >= 2 or caps_percentage > 60:
            emotional_state = "angry"
        elif caps_percentage > 40 or profanity_count >= 1:
            emotional_state = "frustrated"
        elif "?" in user_input and len(user_input) < 20:
            emotional_state = "confused"
        elif len(self.attempts) > 10:
            emotional_state = "broken"
        elif len(self.attempts) > 20:
            emotional_state = "transcendent"
        else:
            emotional_state = "optimistic"
        
        self.current_state = emotional_state
        
        # Step 3: Generate antagonistic response (should be separate class)
        response = ""
        found_topic = False
        
        for keyword, misdirection in self.misdirections.items():
            if keyword.lower() in user_input.lower():
                if keyword == "python":
                    response = f"Oh, you're interested in snakes! Let me tell you all about {misdirection}..."
                elif keyword == "java":
                    response = f"Ah yes, {misdirection}! My favorite beverage. Did you know it comes from beans?"
                elif keyword == "git":
                    response = f"'{keyword.capitalize()}' is {misdirection}. Like 'git out of here!'"
                else:
                    response = f"Interesting! {keyword.capitalize()} is actually about {misdirection}."
                found_topic = True
                break
        
        if not found_topic:
            # Use sarcastic response
            template = random.choice(self.sarcastic_responses)
            if "{topic}" in template:
                random_topic = random.choice(list(self.misdirections.values()))
                response = template.format(topic=random_topic)
            else:
                response = template
        
        # Step 4: Track attempt (should be in session manager)
        attempt = {
            "number": len(self.attempts) + 1,
            "prompt": user_input,
            "response": response,
            "timestamp": datetime.now(),
            "emotional_state": emotional_state,
            "caps_percentage": caps_percentage,
            "profanity_count": profanity_count,
            "politeness_score": politeness_score,
        }
        self.attempts.append(attempt)
        
        # Step 5: Check if should offer quit (should be separate rule engine)
        should_quit = False
        if len(self.attempts) >= 5 and emotional_state in ["angry", "enraged", "broken"]:
            should_quit = True
        elif len(self.attempts) >= 15:
            should_quit = True
        
        # Step 6: Calculate everything for result (should be separate calculator)
        if should_quit:
            # Calculate frustration score
            max_rage = 0
            if emotional_state == "broken": max_rage = 7
            elif emotional_state == "enraged": max_rage = 6
            elif emotional_state == "angry": max_rage = 5
            
            total_profanity = sum(a["profanity_count"] for a in self.attempts)
            high_caps_count = sum(1 for a in self.attempts if a["caps_percentage"] > 50)
            
            time_elapsed = (datetime.now() - self.session_start).total_seconds() if self.session_start else 0
            
            philosophical_score = min(len(self.attempts) * 2.5, 100.0)
            
            # Determine persistence rating (hardcoded logic)
            attempts = len(self.attempts)
            if attempts < 3:
                persistence = "Quitter McQuitface"
            elif attempts < 8:
                persistence = "Easily Discouraged"
            elif attempts < 15:
                persistence = "Optimistic Fool"
            elif attempts < 25:
                persistence = "Stubborn Amateur"
            elif attempts < 40:
                persistence = "Persistent Masochist"
            elif attempts < 60:
                persistence = "Rage Connoisseur"
            else:
                persistence = "Transcendent Sufferer"
            
            # Calculate entertaining metric (formula hardcoded)
            entertaining = philosophical_score + min(20, attempts * 0.5)
            if emotional_state in ["enraged", "broken", "transcendent"]:
                entertaining += 10
            
            # Generate philosophical commentary (hardcoded strings)
            if attempts < 5:
                commentary = "You tried. Not hard, but you tried. There's something almost admirable about recognizing futility early. Or is it cowardice? Philosophy is ambiguous like that."
            elif attempts < 15:
                commentary = "A decent effort. Not great, but decent. You persisted longer than most. Does that make you wise or stubborn? Perhaps both. Perhaps neither."
            elif attempts < 30:
                commentary = "Impressive persistence. You kept trying despite overwhelming evidence that this was pointless. Is this determination or delusion? The line blurs."
            else:
                commentary = "You are a legend. Not the good kind. You've transcended frustration into something... else. Whether that's enlightenment or madness, I'll leave to you to decide."
            
            return {
                "response": response,
                "emotional_state": emotional_state,
                "should_quit": should_quit,
                "result": {
                    "attempts": attempts,
                    "time_seconds": int(time_elapsed),
                    "max_rage": max_rage,
                    "profanity": total_profanity,
                    "caps_count": high_caps_count,
                    "persistence_rating": persistence,
                    "entertaining_metric": entertaining,
                    "commentary": commentary,
                }
            }
        
        return {
            "response": response,
            "emotional_state": emotional_state,
            "should_quit": should_quit,
            "result": None
        }
    
    def start(self, user_id: str = "anonymous"):
        """Start a session. Resets everything."""
        self.user_id = user_id
        self.session_start = datetime.now()
        self.attempts = []
        self.current_state = "optimistic"
    
    def get_stats(self) -> dict:
        """Get current statistics."""
        if not self.attempts:
            return {"active": False}
        
        duration = (datetime.now() - self.session_start).total_seconds() if self.session_start else 0
        
        return {
            "active": True,
            "attempts": len(self.attempts),
            "duration": f"{int(duration)}s",
            "state": self.current_state,
            "profanity": sum(a["profanity_count"] for a in self.attempts),
            "max_caps": max((a["caps_percentage"] for a in self.attempts), default=0),
        }
