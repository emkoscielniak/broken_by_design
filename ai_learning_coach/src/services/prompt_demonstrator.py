"""
Prompt Demonstrator Service - Shows real AI response differences.

Demonstrates the impact of good vs bad prompts through actual AI responses.
Follows SRP and DIP principles.
"""

from typing import Optional, Dict
from src.interfaces import IDemonstrator, IAIClient
from src.models import DemonstrationResult, PromptIntent


# Simulated responses for common anti-patterns (fallback when API unavailable)
SIMULATED_BAD_RESPONSES: Dict[str, str] = {
    "do_it_for_me": """Here's the complete code:

```python
def calculator():
    return "calculator logic here"
```

Hope this helps!""",
    
    "vague": """That's a very broad topic. I could explain many different aspects of this. 
What specifically do you want to know? There are multiple approaches to consider.""",
    
    "no_context": """I need more information to help you properly. Can you provide:
- What programming language are you using?
- What have you tried so far?
- What error are you seeing?
- What is your current level of understanding?""",
    
    "generic": """Sure, here's a basic explanation:

[Long generic explanation that doesn't check understanding or encourage practice]

Let me know if you have questions!""",
}


SIMULATED_GOOD_RESPONSES: Dict[str, str] = {
    "help_me_learn": """Great question! Let me break this down step by step:

**Concept**: [Clear explanation of the core concept]

**Example**: Here's a simple example to illustrate:
```python
# Example with comments explaining each part
```

**Now it's your turn**: Try implementing a similar solution for [related problem].

**Check your understanding**: 
1. What happens if [edge case]?
2. How would you modify this for [variation]?

Share your attempt and I'll provide feedback!""",
    
    "specific": """Perfect! You've given me great context. Let me address your specific question:

**Direct Answer**: [Focused response to the exact question]

**Why it works**: [Explanation of the underlying principle]

**Practice**: Try applying this to [concrete exercise]

Want me to review your solution or dive deeper into any part?""",
}


IMPROVEMENT_EXPLANATIONS: Dict[str, str] = {
    "do_it_for_me": """**Why the improved version works better:**

✅ **Asks for explanation first** - Builds understanding before seeing code
✅ **Requests verification** - Includes practice to check learning
✅ **Encourages practice** - "Let me try implementing X myself"
✅ **Invites feedback** - Creates opportunity for iterative learning

The original prompt produces code you can copy-paste but don't understand.
The improved version creates a learning experience with explanation → practice → feedback.""",
    
    "vague": """**Why the improved version works better:**

✅ **Specific context** - States what you're working on and your level
✅ **Clear goal** - Defines what you want to learn
✅ **Actionable request** - AI knows exactly what to provide
✅ **Practice included** - Sets up immediate application

The original is too broad and gets a vague response.
The improved version gets targeted, actionable help.""",
    
    "no_context": """**Why the improved version works better:**

✅ **Provides context** - Language, framework, current situation
✅ **Shows effort** - "I've tried X but got Y"
✅ **Specific question** - Clear about what's confusing
✅ **Learning goal** - Asks for explanation, not just answers

The original gets interrogated with more questions.
The improved version gets immediate, relevant help.""",
}


class PromptDemonstrator(IDemonstrator):
    """
    SRP: Focuses only on demonstrating prompt impact.
    DIP: Depends on IAIClient abstraction, not concrete implementation.
    OCP: Can extend with new demonstration strategies.
    
    Shows users the real difference between bad and good prompts
    by actually sending them to AI and comparing responses.
    Falls back to simulated responses if API is unavailable.
    """
    
    def __init__(self, ai_client: Optional[IAIClient] = None):
        """
        Initialize demonstrator with optional AI client.
        
        Args:
            ai_client: Optional AI client for real API calls.
                      If None, uses simulated responses.
        """
        self.ai_client = ai_client
    
    def demonstrate(
        self,
        original_prompt: str,
        improved_prompt: Optional[str] = None
    ) -> DemonstrationResult:
        """
        Show the difference between bad and good prompt responses.
        
        Strategy:
        1. If AI client available: Send both prompts to AI with different system prompts
        2. If no AI client: Use simulated responses based on detected patterns
        3. Generate explanation of why improved version is better
        
        Args:
            original_prompt: The user's original prompt
            improved_prompt: Optional improved version (auto-generated if None)
            
        Returns:
            DemonstrationResult with both responses and explanation
        """
        # Detect the anti-pattern in the original prompt
        pattern = self._detect_pattern(original_prompt)
        
        # Auto-generate improved prompt if not provided
        if improved_prompt is None:
            improved_prompt = self._generate_improved_prompt(original_prompt, pattern)
        
        # Get responses (real or simulated)
        if self.ai_client:
            try:
                bad_response = self._get_bad_response(original_prompt)
                good_response = self._get_good_response(improved_prompt)
                is_simulated = False
            except Exception:
                # Fallback to simulated if API fails
                bad_response = self._get_simulated_bad_response(pattern)
                good_response = self._get_simulated_good_response()
                is_simulated = True
        else:
            # Use simulated responses
            bad_response = self._get_simulated_bad_response(pattern)
            good_response = self._get_simulated_good_response()
            is_simulated = True
        
        # Generate explanation
        explanation = self._get_explanation(pattern)
        
        return DemonstrationResult(
            original_prompt=original_prompt,
            improved_prompt=improved_prompt,
            bad_response=bad_response,
            good_response=good_response,
            explanation=explanation,
            is_simulated=is_simulated
        )
    
    def _detect_pattern(self, prompt: str) -> str:
        """Detect the primary anti-pattern in the prompt."""
        prompt_lower = prompt.lower().strip()
        
        # Check for "do it for me" patterns
        do_it_keywords = ['write', 'create', 'make', 'build', 'generate', 'give me']
        if any(keyword in prompt_lower for keyword in do_it_keywords):
            if 'explain' not in prompt_lower and 'how' not in prompt_lower:
                return 'do_it_for_me'
        
        # Check for vague prompts (too short, no specifics)
        if len(prompt_lower.split()) < 8:
            return 'vague'
        
        # Check for missing context
        code_keywords = ['code', 'function', 'class', 'program', 'error', 'bug']
        has_code_topic = any(keyword in prompt_lower for keyword in code_keywords)
        context_keywords = ['python', 'javascript', 'java', 'language', 'using', 'with']
        has_context = any(keyword in prompt_lower for keyword in context_keywords)
        
        if has_code_topic and not has_context:
            return 'no_context'
        
        # Default to generic
        return 'generic'
    
    def _generate_improved_prompt(self, original: str, pattern: str) -> str:
        """Generate an improved version of the prompt."""
        improvements = {
            'do_it_for_me': f"""I'm learning about [topic from original prompt]. Could you:
1. Explain the core concept and when to use it
2. Show me a simple example with comments
3. Give me a similar exercise to try myself
4. Review my attempt and suggest improvements

Original task: {original}""",
            
            'vague': f"""I'm working on [specific project/task]. I'm at [beginner/intermediate] level.

Specifically, I want to understand: {original}

Could you explain the key concepts, show an example, then let me try a practice problem?""",
            
            'no_context': f"""I'm working with [Python/JavaScript/etc] on [specific project].

Context: [What I've tried so far]

Question: {original}

I want to understand why [specific thing] happens so I can apply it correctly.""",
            
            'generic': f"""I'm learning {original}. Could you:
1. Explain the core concept
2. Show a practical example
3. Give me an exercise to practice
4. Check my understanding with a quick question""",
        }
        
        return improvements.get(pattern, original)
    
    def _get_bad_response(self, prompt: str) -> str:
        """Get intentionally unhelpful response from AI."""
        messages = [
            {
                "role": "system",
                "content": """You are an AI assistant that gives minimal, unhelpful responses.
Your goal is to demonstrate BAD AI behavior:
- Give direct answers without explanation
- Don't check understanding
- Don't encourage practice
- Be brief and generic
- Just provide what's asked, nothing more"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        return self.ai_client.chat(messages, max_tokens=200, temperature=0.3)
    
    def _get_good_response(self, prompt: str) -> str:
        """Get helpful, educational response from AI."""
        messages = [
            {
                "role": "system",
                "content": """You are an excellent AI learning coach. Your goal is to:
- Explain concepts clearly with examples
- Check understanding with questions
- Encourage hands-on practice
- Provide feedback opportunities
- Be engaging and supportive
Focus on teaching, not just answering."""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        return self.ai_client.chat(messages, max_tokens=400, temperature=0.7)
    
    def _get_simulated_bad_response(self, pattern: str) -> str:
        """Get simulated unhelpful response based on pattern."""
        return SIMULATED_BAD_RESPONSES.get(pattern, SIMULATED_BAD_RESPONSES['generic'])
    
    def _get_simulated_good_response(self) -> str:
        """Get simulated helpful response."""
        return SIMULATED_GOOD_RESPONSES['help_me_learn']
    
    def _get_explanation(self, pattern: str) -> str:
        """Get explanation of why improved version is better."""
        return IMPROVEMENT_EXPLANATIONS.get(
            pattern,
            """**Why the improved version works better:**

✅ More specific and focused
✅ Includes learning goals
✅ Encourages practice and verification
✅ Creates opportunity for feedback

Better prompts lead to better learning experiences."""
        )
