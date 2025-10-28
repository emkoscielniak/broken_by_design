"""
FeedbackGenerator service implementation.

This service generates user-friendly feedback based on prompt analysis,
supporting multiple feedback styles (encouraging, direct, Socratic).

Demonstrates:
- SRP: Single responsibility of generating feedback
- OCP: Open for extension via new feedback styles
- LSP: Implements IFeedbackProvider interface
"""

from typing import Literal
from src.interfaces import IFeedbackProvider
from src.models import PromptAnalysis


FeedbackStyle = Literal["encouraging", "direct", "socratic"]


class FeedbackGenerator(IFeedbackProvider):
    """
    Generates personalized feedback for prompt analysis.
    
    Supports three feedback styles:
    - encouraging: Positive, motivational tone
    - direct: Straightforward, factual tone
    - socratic: Question-based, reflective tone
    """
    
    def __init__(self, style: FeedbackStyle = "encouraging"):
        """
        Initialize feedback generator with a style.
        
        Args:
            style: The feedback style to use (encouraging, direct, or socratic)
        """
        valid_styles = ["encouraging", "direct", "socratic"]
        self.style = style if style in valid_styles else "encouraging"
    
    def generate_feedback(self, analysis: PromptAnalysis) -> str:
        """
        Generate feedback based on prompt analysis.
        
        Args:
            analysis: The prompt analysis results
            
        Returns:
            Formatted feedback string
        """
        if self.style == "encouraging":
            return self._generate_encouraging_feedback(analysis)
        elif self.style == "direct":
            return self._generate_direct_feedback(analysis)
        else:  # socratic
            return self._generate_socratic_feedback(analysis)
    
    def _generate_encouraging_feedback(self, analysis: PromptAnalysis) -> str:
        """Generate encouraging, positive feedback."""
        parts = []
        score = analysis.score
        
        # Opening based on score
        if score.total_score >= 80:
            parts.append(f"🌟 Excellent work! Your prompt scored {score.total_score:.0f}/100.")
        elif score.total_score >= 60:
            parts.append(f"👍 Good effort! Your prompt scored {score.total_score:.0f}/100.")
        else:
            parts.append(f"Thanks for trying! Your prompt scored {score.total_score:.0f}/100. Let's improve it together!")
        
        # Strengths
        if analysis.strengths:
            parts.append("\n✨ What you did well:")
            for strength in analysis.strengths:
                parts.append(f"  • {strength}")
        
        # Anti-patterns (if any)
        if analysis.detected_patterns:
            parts.append("\n⚠️  Patterns to avoid:")
            for pattern in analysis.detected_patterns:
                parts.append(f"  • {pattern}")
        
        # Improvements
        if analysis.improvements:
            parts.append("\n💡 Ways to improve:")
            for improvement in analysis.improvements:
                parts.append(f"  • {improvement}")
        
        # Examples
        if analysis.examples:
            parts.append("\n📝 Try these instead:")
            for example in analysis.examples[:2]:  # Limit to 2 examples
                parts.append(f"  • {example}")
        
        # Closing encouragement
        if score.total_score >= 60:
            parts.append("\n🎉 Keep up the great work! You're learning effectively!")
        else:
            parts.append("\n💪 You've got this! Small improvements will make a big difference!")
        
        return "\n".join(parts)
    
    def _generate_direct_feedback(self, analysis: PromptAnalysis) -> str:
        """Generate direct, factual feedback."""
        parts = []
        score = analysis.score
        
        # Score report
        parts.append(f"Prompt Score: {score.total_score:.0f}/100")
        parts.append(f"  - Learning Orientation: {score.learning_orientation:.0f}/100")
        parts.append(f"  - Specificity: {score.specificity:.0f}/100")
        parts.append(f"  - Engagement: {score.engagement:.0f}/100")
        parts.append(f"  - Intent: {score.intent.value}")
        
        # Status
        if score.is_passing:
            parts.append("\nStatus: PASSING - This prompt demonstrates good learning practices.")
        else:
            parts.append("\nStatus: NEEDS IMPROVEMENT - This prompt needs refinement.")
        
        # Detected issues
        if analysis.detected_patterns:
            parts.append("\nDetected Issues:")
            for i, pattern in enumerate(analysis.detected_patterns, 1):
                parts.append(f"{i}. {pattern}")
        
        # Strengths
        if analysis.strengths:
            parts.append("\nStrengths:")
            for i, strength in enumerate(analysis.strengths, 1):
                parts.append(f"{i}. {strength}")
        
        # Required improvements
        if analysis.improvements:
            parts.append("\nRequired Improvements:")
            for i, improvement in enumerate(analysis.improvements, 1):
                parts.append(f"{i}. {improvement}")
        
        # Examples
        if analysis.examples:
            parts.append("\nBetter Alternatives:")
            for example in analysis.examples[:3]:
                parts.append(f"  {example}")
        
        return "\n".join(parts)
    
    def _generate_socratic_feedback(self, analysis: PromptAnalysis) -> str:
        """Generate Socratic, question-based feedback."""
        parts = []
        score = analysis.score
        
        # Opening question
        parts.append(f"Your prompt scored {score.total_score:.0f}/100. Let's reflect on this together.\n")
        
        # Questions about intent
        if score.intent.value == "do_it_for_me":
            parts.append("🤔 Consider this: Are you asking the AI to do your work, or to help you learn?")
            parts.append("What would happen if you asked for guidance instead of a complete solution?\n")
        
        # Questions about strengths
        if analysis.strengths:
            parts.append("What you did well:")
            for strength in analysis.strengths:
                parts.append(f"  ✓ {strength}")
            parts.append("\nHow can you build on these strengths in your next prompt?\n")
        
        # Questions about weaknesses
        if score.learning_orientation < 60:
            parts.append("❓ Could you rephrase your request to focus on understanding rather than completion?")
        
        if score.specificity < 60:
            parts.append("❓ What specific aspect or detail could you add to make your question clearer?")
        
        if score.engagement < 60:
            parts.append("❓ How might you make this more interactive? Could you ask for examples, quizzes, or practice?")
        
        # Reflective closing
        if analysis.detected_patterns:
            parts.append("\n⚠️  Patterns detected:")
            for pattern in analysis.detected_patterns:
                parts.append(f"  • {pattern}")
            parts.append("\nWhat changes could address these patterns?")
        
        # Example questions
        if analysis.examples:
            parts.append("\n💭 Compare your prompt to these alternatives:")
            for example in analysis.examples[:2]:
                parts.append(f"  • {example}")
            parts.append("\nWhat makes these examples more effective for learning?")
        
        return "\n".join(parts)
