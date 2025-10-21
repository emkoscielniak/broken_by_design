# AI Learning Coach - Architecture Document

**Version:** 1.0  
**Date:** October 21, 2025  
**Purpose:** Teach effective AI prompting through interactive lessons and real-time feedback

---

## 1. Executive Summary

### 1.1 Project Vision
An interactive CLI application that teaches users how to effectively prompt AI assistants for learning. The system provides guided lessons, analyzes user prompts, gives constructive feedback, and demonstrates the difference between "do it for me" vs "help me learn" approaches.

### 1.2 Core Philosophy
**Bad Prompting:** "Write my essay about climate change"  
**Good Prompting:** "Explain the greenhouse effect using an analogy, then ask me questions to check my understanding"

### 1.3 Learning Outcomes
- Understand effective vs ineffective prompts
- Learn to ask clarifying questions instead of solutions
- Practice scaffolded learning with AI
- Develop metacognitive awareness about learning
- Build a personal prompt library

---

## 2. SOLID Principles Application

### 2.1 Single Responsibility Principle (SRP)
Each class has ONE reason to change:

- **PromptAnalyzer**: Analyzes prompt quality (scoring, pattern detection)
- **LessonManager**: Manages lesson content and progression
- **FeedbackGenerator**: Creates constructive feedback messages
- **OpenAIClient**: Handles API communication only
- **UserProgressTracker**: Stores and retrieves user progress
- **ConversationLogger**: Logs interactions for review

### 2.2 Open/Closed Principle (OCP)
Open for extension, closed for modification:

- **Base Lesson class**: Can extend with new lesson types without modifying core
- **Strategy Pattern for Scoring**: Add new scoring algorithms without changing analyzer
- **Plugin system for Prompt Patterns**: Add new anti-patterns without core changes

### 2.3 Liskov Substitution Principle (LSP)
Subtypes are substitutable:

- **Lesson** → `BasicLesson`, `AdvancedLesson`, `InteractiveLesson` (all work with LessonManager)
- **ScoreStrategy** → `RubricScorer`, `AIScorer`, `HybridScorer` (all return compatible scores)
- **FeedbackProvider** → `DetailedFeedback`, `ConciseFeedback`, `BeginnnerFeedback`

### 2.4 Interface Segregation Principle (ISP)
Clients shouldn't depend on interfaces they don't use:

- **IPromptEvaluator**: Just `evaluate(prompt) -> Score`
- **ILessonProvider**: Just `get_lesson(level) -> Lesson`
- **IProgressPersister**: Just `save(data)` and `load() -> data`
- **IAIClient**: Just `chat(messages) -> response`

### 2.5 Dependency Inversion Principle (DIP)
Depend on abstractions, not concretions:

- High-level `LearningCoach` depends on `IAIClient` interface (not OpenAI directly)
- `PromptAnalyzer` depends on `IScoreStrategy` interface
- `UserProgressTracker` depends on `IProgressPersister` (could be JSON, DB, etc.)

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI Interface Layer                       │
│              (User Interaction & Display)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Application Layer                           │
│           (LearningCoach - Main Orchestrator)               │
└────────┬─────────────┬──────────────┬────────────┬──────────┘
         │             │              │            │
    ┌────▼───┐   ┌────▼────┐   ┌─────▼─────┐ ┌───▼────────┐
    │Lesson  │   │Prompt   │   │Feedback   │ │Progress    │
    │Manager │   │Analyzer │   │Generator  │ │Tracker     │
    └────┬───┘   └────┬────┘   └─────┬─────┘ └───┬────────┘
         │            │               │            │
         │       ┌────▼────────┐      │            │
         │       │Score        │      │            │
         │       │Strategy     │      │            │
         │       └─────────────┘      │            │
         │                            │            │
    ┌────▼────────────────────────────▼────────────▼─────────┐
    │              Infrastructure Layer                       │
    │  (OpenAI Client, File Storage, Logging)                │
    └─────────────────────────────────────────────────────────┘
```

### 3.2 Component Diagram with SOLID Principles

```
┌─────────────────────────────────────────────────┐
│         LearningCoach (Orchestrator)            │
│  - SRP: Coordinates learning flow only          │
│  - DIP: Depends on abstractions                 │
└──┬────────┬──────────┬──────────┬──────────────┘
   │        │          │          │
   │   Implements interfaces (DIP)
   │        │          │          │
   ▼        ▼          ▼          ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐
│ILesson││IPrompt││IFeed││IProgress │
│Provider│Eval   ││back ││Tracker   │
└───────┘└───────┘└─────┘└──────────┘
   │        │        │        │
   │        │        │        │
   ▼        ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐
│Lesson│ │Prompt│ │Feed  │ │Progress  │
│Mgr   │ │Analyz│ │Gen   │ │Tracker   │
│      │ │er    │ │      │ │          │
│-SRP  │ │-SRP  │ │-SRP  │ │-SRP      │
│-OCP  │ │-OCP  │ │-OCP  │ │-OCP      │
└──────┘ └──┬───┘ └──────┘ └──────────┘
            │
            │ Uses (DIP)
            ▼
      ┌──────────┐
      │IScore    │
      │Strategy  │
      └────┬─────┘
           │
     ┌─────┴──────┐
     ▼            ▼
┌─────────┐  ┌─────────┐
│Rubric   │  │AI       │
│Scorer   │  │Scorer   │
│(LSP)    │  │(LSP)    │
└─────────┘  └─────────┘
```

---

## 4. Core Components (SOLID Implementation)

### 4.1 Data Models (`src/models/`)

#### 4.1.1 Prompt Models
```python
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class PromptIntent(Enum):
    """Types of prompt intents"""
    DO_IT_FOR_ME = "do_it_for_me"      # Bad: "Write my essay"
    HELP_ME_LEARN = "help_me_learn"    # Good: "Explain and quiz me"
    CLARIFYING = "clarifying"          # Good: "What do you mean by X?"
    REFLECTION = "reflection"          # Good: "How does this relate to Y?"
    UNKNOWN = "unknown"

@dataclass
class PromptScore:
    """
    SRP: Only represents score data
    Immutable value object
    """
    total_score: float  # 0-100
    learning_orientation: float  # 0-100
    specificity: float  # 0-100
    engagement: float  # 0-100
    intent: PromptIntent
    
    @property
    def is_passing(self) -> bool:
        """Minimum 60% to pass"""
        return self.total_score >= 60.0

@dataclass
class PromptAnalysis:
    """
    SRP: Complete analysis results
    Contains score + detailed feedback
    """
    prompt: str
    score: PromptScore
    strengths: List[str]
    improvements: List[str]
    examples: List[str]
    detected_patterns: List[str]  # Anti-patterns found

@dataclass
class Lesson:
    """
    SRP: Lesson content only
    OCP: Can extend with new lesson types
    """
    id: str
    title: str
    description: str
    learning_objectives: List[str]
    difficulty: int  # 1-5
    content: str
    exercises: List['Exercise']
    
@dataclass
class Exercise:
    """Practice exercise within a lesson"""
    id: str
    prompt: str
    expected_intent: PromptIntent
    hints: List[str]
    good_example: str
    bad_example: str

@dataclass
class UserProgress:
    """
    SRP: User state tracking only
    """
    user_id: str
    current_lesson: int
    completed_lessons: List[str]
    prompt_history: List[PromptAnalysis]
    skill_level: int  # 1-5
    total_prompts: int
    good_prompts: int  # Score >= 60
```

#### 4.1.2 Configuration Models
```python
@dataclass
class CoachConfig:
    """
    SRP: Configuration data only
    Immutable settings
    """
    api_key: str
    model: str = "gpt-4o-mini"
    feedback_style: str = "detailed"  # detailed, concise, beginner
    auto_advance: bool = False
    save_history: bool = True
    
@dataclass
class ScoreWeights:
    """
    SRP: Scoring configuration
    OCP: Can add new weights without changing scoring logic
    """
    learning_orientation: float = 0.4
    specificity: float = 0.3
    engagement: float = 0.3
```

---

### 4.2 Interfaces (`src/interfaces/`)

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from src.models import (
    PromptAnalysis, PromptScore, Lesson, 
    UserProgress, CoachConfig
)

class IPromptEvaluator(ABC):
    """
    ISP: Focused interface for prompt evaluation
    DIP: High-level modules depend on this abstraction
    """
    @abstractmethod
    def evaluate(self, prompt: str, context: Optional[str] = None) -> PromptAnalysis:
        """Analyze a prompt and return detailed analysis"""
        pass

class IScoreStrategy(ABC):
    """
    ISP: Focused on scoring only
    OCP: Can add new strategies without changing evaluator
    """
    @abstractmethod
    def calculate_score(self, prompt: str, context: Optional[str] = None) -> PromptScore:
        """Calculate score for a prompt"""
        pass

class ILessonProvider(ABC):
    """
    ISP: Focused on lesson retrieval
    DIP: LearningCoach depends on this, not concrete implementation
    """
    @abstractmethod
    def get_lesson(self, lesson_id: str) -> Lesson:
        """Get specific lesson by ID"""
        pass
    
    @abstractmethod
    def get_lessons_by_level(self, level: int) -> List[Lesson]:
        """Get all lessons for a skill level"""
        pass
    
    @abstractmethod
    def get_next_lesson(self, current_lesson_id: str) -> Optional[Lesson]:
        """Get next lesson in sequence"""
        pass

class IFeedbackProvider(ABC):
    """
    ISP: Focused on feedback generation
    OCP: Can add new feedback styles
    """
    @abstractmethod
    def generate_feedback(self, analysis: PromptAnalysis) -> str:
        """Generate human-readable feedback"""
        pass

class IProgressPersister(ABC):
    """
    ISP: Focused on persistence only
    DIP: Allows swapping storage backends
    """
    @abstractmethod
    def save(self, progress: UserProgress) -> None:
        """Save user progress"""
        pass
    
    @abstractmethod
    def load(self, user_id: str) -> UserProgress:
        """Load user progress"""
        pass

class IAIClient(ABC):
    """
    ISP: Minimal AI interaction interface
    DIP: Allows mocking for tests, swapping providers
    """
    @abstractmethod
    def chat(self, messages: List[dict], **kwargs) -> str:
        """Send chat messages and get response"""
        pass
    
    @abstractmethod
    def analyze_prompt_intent(self, prompt: str) -> dict:
        """Use AI to analyze prompt intent"""
        pass
```

---

### 4.3 Core Services (`src/services/`)

#### 4.3.1 Prompt Analyzer (SRP, OCP, DIP)
```python
from src.interfaces import IPromptEvaluator, IScoreStrategy
from src.models import PromptAnalysis, PromptScore
from typing import List, Optional

class PromptAnalyzer(IPromptEvaluator):
    """
    SRP: Only analyzes prompts
    DIP: Depends on IScoreStrategy abstraction
    OCP: Can extend with new analysis methods
    
    This class coordinates scoring and pattern detection
    but delegates actual scoring to a strategy.
    """
    
    def __init__(self, score_strategy: IScoreStrategy):
        """
        DIP: Inject scoring strategy (not hardcoded)
        Allows easy testing and strategy swapping
        """
        self.score_strategy = score_strategy
        self.anti_patterns = self._load_anti_patterns()
    
    def evaluate(self, prompt: str, context: Optional[str] = None) -> PromptAnalysis:
        """
        Main analysis method
        Coordinates all analysis activities
        """
        # Calculate score using injected strategy
        score = self.score_strategy.calculate_score(prompt, context)
        
        # Detect patterns
        detected = self._detect_patterns(prompt)
        
        # Generate insights
        strengths = self._identify_strengths(prompt, score)
        improvements = self._identify_improvements(prompt, score, detected)
        examples = self._generate_examples(prompt)
        
        return PromptAnalysis(
            prompt=prompt,
            score=score,
            strengths=strengths,
            improvements=improvements,
            examples=examples,
            detected_patterns=detected
        )
    
    def _detect_patterns(self, prompt: str) -> List[str]:
        """
        SRP: Pattern detection only
        Looks for anti-patterns in the prompt
        """
        detected = []
        
        for pattern_name, pattern_info in self.anti_patterns.items():
            if self._matches_pattern(prompt, pattern_info):
                detected.append(pattern_name)
        
        return detected
    
    def _matches_pattern(self, prompt: str, pattern_info: dict) -> bool:
        """Check if prompt matches an anti-pattern"""
        keywords = pattern_info.get('keywords', [])
        return any(keyword.lower() in prompt.lower() for keyword in keywords)
    
    def _identify_strengths(self, prompt: str, score: PromptScore) -> List[str]:
        """Identify what the user did well"""
        strengths = []
        
        if score.learning_orientation > 70:
            strengths.append("Shows learning intent (asking for understanding, not just answers)")
        
        if score.specificity > 70:
            strengths.append("Specific and clear about what you need")
        
        if score.engagement > 70:
            strengths.append("Encourages interactive learning")
        
        if "?" in prompt:
            strengths.append("Asks questions (good learning behavior)")
        
        return strengths
    
    def _identify_improvements(
        self, prompt: str, score: PromptScore, patterns: List[str]
    ) -> List[str]:
        """Suggest improvements"""
        improvements = []
        
        if score.learning_orientation < 50:
            improvements.append(
                "Focus on learning, not just getting answers. "
                "Try: 'Explain X and quiz me' instead of 'Tell me X'"
            )
        
        if score.specificity < 50:
            improvements.append(
                "Be more specific about what you want to learn"
            )
        
        if "do_it_for_me" in patterns:
            improvements.append(
                "Avoid asking AI to do your work. "
                "Ask it to teach you how to do it yourself"
            )
        
        return improvements
    
    def _generate_examples(self, prompt: str) -> List[str]:
        """Generate better versions of the prompt"""
        # This would use templates or AI to generate examples
        return []
    
    def _load_anti_patterns(self) -> dict:
        """
        OCP: Load patterns from config
        Can add new patterns without code changes
        """
        return {
            "do_it_for_me": {
                "keywords": ["write my", "do my", "create my", "solve this for me"],
                "description": "Asking AI to complete work instead of learning"
            },
            "no_engagement": {
                "keywords": ["just tell me", "give me the answer", "what is"],
                "description": "Passive information request without learning intent"
            },
            "too_vague": {
                "keywords": ["help me", "explain", "tell me about"],
                "description": "Too vague, lacks specific learning goal"
            }
        }
```

#### 4.3.2 Score Strategies (OCP, LSP)
```python
from src.interfaces import IScoreStrategy
from src.models import PromptScore, PromptIntent, ScoreWeights
from typing import Optional

class RubricScorer(IScoreStrategy):
    """
    LSP: Can substitute for IScoreStrategy
    OCP: Scoring logic isolated, can be extended
    
    Uses rule-based rubric to score prompts
    Fast, predictable, no API calls needed
    """
    
    def __init__(self, weights: Optional[ScoreWeights] = None):
        self.weights = weights or ScoreWeights()
    
    def calculate_score(self, prompt: str, context: Optional[str] = None) -> PromptScore:
        """Calculate score using rubric"""
        learning = self._score_learning_orientation(prompt)
        specificity = self._score_specificity(prompt)
        engagement = self._score_engagement(prompt)
        intent = self._classify_intent(prompt)
        
        total = (
            learning * self.weights.learning_orientation +
            specificity * self.weights.specificity +
            engagement * self.weights.engagement
        )
        
        return PromptScore(
            total_score=total,
            learning_orientation=learning,
            specificity=specificity,
            engagement=engagement,
            intent=intent
        )
    
    def _score_learning_orientation(self, prompt: str) -> float:
        """Score how learning-focused the prompt is"""
        score = 50.0  # Base score
        
        learning_keywords = [
            "explain", "teach", "help me understand", 
            "why", "how does", "can you show me"
        ]
        anti_keywords = [
            "write my", "do my", "give me the answer"
        ]
        
        for keyword in learning_keywords:
            if keyword in prompt.lower():
                score += 10
        
        for keyword in anti_keywords:
            if keyword in prompt.lower():
                score -= 20
        
        return max(0, min(100, score))
    
    def _score_specificity(self, prompt: str) -> float:
        """Score how specific and clear the prompt is"""
        score = 50.0
        
        # Longer prompts tend to be more specific
        if len(prompt) > 100:
            score += 15
        elif len(prompt) < 20:
            score -= 15
        
        # Questions are often specific
        if "?" in prompt:
            score += 10
        
        # Context words indicate specificity
        context_words = ["because", "specifically", "in the context of"]
        for word in context_words:
            if word in prompt.lower():
                score += 10
        
        return max(0, min(100, score))
    
    def _score_engagement(self, prompt: str) -> float:
        """Score how much the prompt encourages interaction"""
        score = 50.0
        
        engagement_keywords = [
            "quiz me", "test my understanding", "ask me questions",
            "practice", "exercise", "check if"
        ]
        
        for keyword in engagement_keywords:
            if keyword in prompt.lower():
                score += 15
        
        return max(0, min(100, score))
    
    def _classify_intent(self, prompt: str) -> PromptIntent:
        """Classify the prompt's intent"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["write my", "do my", "solve this for me"]):
            return PromptIntent.DO_IT_FOR_ME
        
        if any(word in prompt_lower for word in ["explain", "teach me", "help me understand"]):
            return PromptIntent.HELP_ME_LEARN
        
        if any(word in prompt_lower for word in ["what do you mean", "can you clarify"]):
            return PromptIntent.CLARIFYING
        
        return PromptIntent.UNKNOWN


class AIScorer(IScoreStrategy):
    """
    LSP: Can substitute for IScoreStrategy
    Uses OpenAI to score prompts with nuanced understanding
    More accurate but requires API calls
    """
    
    def __init__(self, ai_client: 'IAIClient', weights: Optional[ScoreWeights] = None):
        """DIP: Depends on IAIClient interface"""
        self.ai_client = ai_client
        self.weights = weights or ScoreWeights()
    
    def calculate_score(self, prompt: str, context: Optional[str] = None) -> PromptScore:
        """Use AI to score the prompt"""
        analysis = self.ai_client.analyze_prompt_intent(prompt)
        
        # Parse AI response into scores
        return PromptScore(
            total_score=analysis['total_score'],
            learning_orientation=analysis['learning_orientation'],
            specificity=analysis['specificity'],
            engagement=analysis['engagement'],
            intent=PromptIntent(analysis['intent'])
        )
```

#### 4.3.3 Lesson Manager (SRP, OCP)
```python
from src.interfaces import ILessonProvider
from src.models import Lesson
from typing import List, Optional
import json
from pathlib import Path

class LessonManager(ILessonProvider):
    """
    SRP: Manages lesson content only
    OCP: Can extend with new lesson sources (DB, API, etc.)
    """
    
    def __init__(self, lessons_dir: str = "data/lessons"):
        """Load lessons from JSON files"""
        self.lessons_dir = Path(lessons_dir)
        self.lessons = self._load_all_lessons()
    
    def get_lesson(self, lesson_id: str) -> Lesson:
        """Get specific lesson by ID"""
        if lesson_id not in self.lessons:
            raise ValueError(f"Lesson {lesson_id} not found")
        return self.lessons[lesson_id]
    
    def get_lessons_by_level(self, level: int) -> List[Lesson]:
        """Get all lessons for a skill level"""
        return [
            lesson for lesson in self.lessons.values()
            if lesson.difficulty == level
        ]
    
    def get_next_lesson(self, current_lesson_id: str) -> Optional[Lesson]:
        """Get next lesson in sequence"""
        # Implementation would follow lesson progression logic
        pass
    
    def _load_all_lessons(self) -> dict:
        """
        OCP: Lesson loading logic
        Can extend to load from different sources
        """
        lessons = {}
        
        if not self.lessons_dir.exists():
            return lessons
        
        for lesson_file in self.lessons_dir.glob("*.json"):
            with open(lesson_file) as f:
                data = json.load(f)
                lesson = self._parse_lesson(data)
                lessons[lesson.id] = lesson
        
        return lessons
    
    def _parse_lesson(self, data: dict) -> Lesson:
        """Parse JSON into Lesson object"""
        # Implementation details
        pass
```

#### 4.3.4 Feedback Generator (SRP, OCP)
```python
from src.interfaces import IFeedbackProvider
from src.models import PromptAnalysis
from typing import Optional

class FeedbackGenerator(IFeedbackProvider):
    """
    SRP: Generates feedback only
    OCP: Can extend with new feedback styles
    """
    
    def __init__(self, style: str = "detailed"):
        """
        Style options:
        - detailed: Comprehensive feedback
        - concise: Brief, actionable points
        - beginner: Simplified language
        """
        self.style = style
    
    def generate_feedback(self, analysis: PromptAnalysis) -> str:
        """Generate feedback based on style"""
        if self.style == "detailed":
            return self._detailed_feedback(analysis)
        elif self.style == "concise":
            return self._concise_feedback(analysis)
        elif self.style == "beginner":
            return self._beginner_feedback(analysis)
        else:
            return self._detailed_feedback(analysis)
    
    def _detailed_feedback(self, analysis: PromptAnalysis) -> str:
        """Comprehensive feedback with examples"""
        lines = []
        lines.append(f"\n{'='*60}")
        lines.append(f"PROMPT ANALYSIS")
        lines.append(f"{'='*60}")
        lines.append(f"\nYour Prompt: \"{analysis.prompt}\"")
        lines.append(f"\nScore: {analysis.score.total_score:.1f}/100")
        
        if analysis.score.is_passing:
            lines.append("✅ PASSING - Good learning-oriented prompt!")
        else:
            lines.append("❌ NEEDS IMPROVEMENT - Let's make this better")
        
        lines.append(f"\n{'─'*60}")
        lines.append("BREAKDOWN:")
        lines.append(f"  Learning Orientation: {analysis.score.learning_orientation:.1f}/100")
        lines.append(f"  Specificity:          {analysis.score.specificity:.1f}/100")
        lines.append(f"  Engagement:           {analysis.score.engagement:.1f}/100")
        lines.append(f"  Intent:               {analysis.score.intent.value}")
        
        if analysis.strengths:
            lines.append(f"\n{'─'*60}")
            lines.append("✨ STRENGTHS:")
            for strength in analysis.strengths:
                lines.append(f"  ✓ {strength}")
        
        if analysis.improvements:
            lines.append(f"\n{'─'*60}")
            lines.append("💡 HOW TO IMPROVE:")
            for improvement in analysis.improvements:
                lines.append(f"  • {improvement}")
        
        if analysis.detected_patterns:
            lines.append(f"\n{'─'*60}")
            lines.append("⚠️  ANTI-PATTERNS DETECTED:")
            for pattern in analysis.detected_patterns:
                lines.append(f"  ⚠  {pattern}")
        
        if analysis.examples:
            lines.append(f"\n{'─'*60}")
            lines.append("📚 BETTER ALTERNATIVES:")
            for i, example in enumerate(analysis.examples, 1):
                lines.append(f"  {i}. \"{example}\"")
        
        lines.append(f"{'='*60}\n")
        
        return "\n".join(lines)
    
    def _concise_feedback(self, analysis: PromptAnalysis) -> str:
        """Brief, actionable feedback"""
        status = "✅ PASS" if analysis.score.is_passing else "❌ IMPROVE"
        return f"{status} ({analysis.score.total_score:.0f}/100): {analysis.improvements[0] if analysis.improvements else 'Good job!'}"
    
    def _beginner_feedback(self, analysis: PromptAnalysis) -> str:
        """Simplified feedback for beginners"""
        # Simplified version with encouraging tone
        pass
```

---

### 4.4 Infrastructure (`src/infrastructure/`)

#### 4.4.1 OpenAI Client (SRP, DIP)
```python
from src.interfaces import IAIClient
from openai import OpenAI
from typing import List, Optional
import os

class OpenAIClient(IAIClient):
    """
    SRP: Only handles OpenAI API communication
    DIP: Implements IAIClient interface
    
    This allows the application to work with any AI provider
    that implements IAIClient
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required")
        self.client = OpenAI(api_key=self.api_key)
    
    def chat(self, messages: List[dict], **kwargs) -> str:
        """Send chat completion request"""
        model = kwargs.get('model', 'gpt-4o-mini')
        
        response = self.client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        return response.choices[0].message.content
    
    def analyze_prompt_intent(self, prompt: str) -> dict:
        """Use AI to analyze a prompt's learning intent"""
        analysis_prompt = f"""
        Analyze this AI prompt for learning effectiveness.
        Score each dimension 0-100:
        
        Prompt: "{prompt}"
        
        Return JSON with:
        - total_score: Overall score (0-100)
        - learning_orientation: Is it asking to learn vs asking for answers?
        - specificity: How clear and specific?
        - engagement: Does it encourage interactive learning?
        - intent: "do_it_for_me", "help_me_learn", "clarifying", or "unknown"
        - reasoning: Brief explanation
        """
        
        messages = [
            {"role": "system", "content": "You are an expert at evaluating learning prompts."},
            {"role": "user", "content": analysis_prompt}
        ]
        
        response = self.chat(messages)
        # Parse JSON response
        import json
        return json.loads(response)
```

#### 4.4.2 Progress Tracker (SRP, DIP)
```python
from src.interfaces import IProgressPersister
from src.models import UserProgress
import json
from pathlib import Path

class JSONProgressPersister(IProgressPersister):
    """
    SRP: Only handles persistence
    DIP: Implements IProgressPersister (could swap to DB)
    OCP: Can extend to support different formats
    """
    
    def __init__(self, data_dir: str = "data/progress"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, progress: UserProgress) -> None:
        """Save progress to JSON file"""
        file_path = self.data_dir / f"{progress.user_id}.json"
        
        with open(file_path, 'w') as f:
            json.dump(self._serialize(progress), f, indent=2)
    
    def load(self, user_id: str) -> UserProgress:
        """Load progress from JSON file"""
        file_path = self.data_dir / f"{user_id}.json"
        
        if not file_path.exists():
            # Return new progress for new user
            return UserProgress(
                user_id=user_id,
                current_lesson=0,
                completed_lessons=[],
                prompt_history=[],
                skill_level=1,
                total_prompts=0,
                good_prompts=0
            )
        
        with open(file_path) as f:
            data = json.load(f)
            return self._deserialize(data)
    
    def _serialize(self, progress: UserProgress) -> dict:
        """Convert UserProgress to dict"""
        # Implementation
        pass
    
    def _deserialize(self, data: dict) -> UserProgress:
        """Convert dict to UserProgress"""
        # Implementation
        pass
```

---

### 4.5 Application Orchestrator (`src/learning_coach.py`)

```python
from src.interfaces import (
    IPromptEvaluator, ILessonProvider, 
    IFeedbackProvider, IProgressPersister, IAIClient
)
from src.models import UserProgress, CoachConfig
from typing import Optional

class LearningCoach:
    """
    Main application orchestrator
    
    SRP: Coordinates the learning flow only
    DIP: Depends on interfaces, not concrete implementations
    OCP: Can extend with new features without modifying
    
    This is the "high-level module" that orchestrates
    everything but doesn't know implementation details.
    """
    
    def __init__(
        self,
        evaluator: IPromptEvaluator,
        lesson_provider: ILessonProvider,
        feedback_provider: IFeedbackProvider,
        progress_persister: IProgressPersister,
        ai_client: IAIClient,
        config: CoachConfig
    ):
        """
        DIP: All dependencies are injected as interfaces
        This makes the class:
        - Easily testable (mock all dependencies)
        - Flexible (swap implementations)
        - Loosely coupled
        """
        self.evaluator = evaluator
        self.lesson_provider = lesson_provider
        self.feedback_provider = feedback_provider
        self.progress_persister = progress_persister
        self.ai_client = ai_client
        self.config = config
        self.current_user: Optional[UserProgress] = None
    
    def start_session(self, user_id: str) -> None:
        """Start a learning session"""
        # Load user progress
        self.current_user = self.progress_persister.load(user_id)
        
        print(f"\n👋 Welcome back! You're on lesson {self.current_user.current_lesson}")
        print(f"📊 Your stats: {self.current_user.good_prompts}/{self.current_user.total_prompts} good prompts")
    
    def practice_prompt(self, user_prompt: str) -> None:
        """
        Main learning interaction
        User submits a prompt, gets analysis and feedback
        """
        # Evaluate the prompt
        analysis = self.evaluator.evaluate(user_prompt)
        
        # Generate feedback
        feedback = self.feedback_provider.generate_feedback(analysis)
        
        # Display feedback
        print(feedback)
        
        # Update progress
        self._update_progress(analysis)
        
        # Save progress
        if self.config.save_history:
            self.progress_persister.save(self.current_user)
    
    def teach_lesson(self, lesson_id: Optional[str] = None) -> None:
        """Teach a specific lesson or continue from progress"""
        if lesson_id is None:
            lesson_id = str(self.current_user.current_lesson)
        
        lesson = self.lesson_provider.get_lesson(lesson_id)
        
        print(f"\n📚 Lesson: {lesson.title}")
        print(f"{lesson.description}\n")
        print(lesson.content)
        
        # Interactive exercises
        for exercise in lesson.exercises:
            self._run_exercise(exercise)
    
    def _run_exercise(self, exercise) -> None:
        """Run an interactive exercise"""
        print(f"\n💪 Exercise: {exercise.prompt}")
        print(f"\n📝 Bad example: \"{exercise.bad_example}\"")
        print(f"✨ Good example: \"{exercise.good_example}\"")
        print("\nNow you try! Write a prompt that demonstrates learning intent:")
        
        # User would input their prompt here
        # Then it gets evaluated
    
    def _update_progress(self, analysis) -> None:
        """Update user progress based on analysis"""
        self.current_user.total_prompts += 1
        
        if analysis.score.is_passing:
            self.current_user.good_prompts += 1
        
        self.current_user.prompt_history.append(analysis)
        
        # Auto-advance if enabled
        if self.config.auto_advance and self._should_advance():
            self.current_user.current_lesson += 1
    
    def _should_advance(self) -> bool:
        """Check if user is ready for next lesson"""
        recent = self.current_user.prompt_history[-5:]
        if len(recent) < 5:
            return False
        
        passing_rate = sum(1 for a in recent if a.score.is_passing) / len(recent)
        return passing_rate >= 0.8  # 80% success rate
    
    def show_progress_report(self) -> None:
        """Display user's learning progress"""
        print(f"\n📊 YOUR PROGRESS REPORT")
        print(f"{'='*60}")
        print(f"Skill Level: {self.current_user.skill_level}/5")
        print(f"Current Lesson: {self.current_user.current_lesson}")
        print(f"Completed Lessons: {len(self.current_user.completed_lessons)}")
        print(f"Total Prompts: {self.current_user.total_prompts}")
        print(f"Good Prompts: {self.current_user.good_prompts}")
        
        if self.current_user.total_prompts > 0:
            success_rate = self.current_user.good_prompts / self.current_user.total_prompts * 100
            print(f"Success Rate: {success_rate:.1f}%")
    
    def end_session(self) -> None:
        """End session and save progress"""
        self.progress_persister.save(self.current_user)
        print("\n👋 Session saved! See you next time!")
```

---

## 5. Testing Strategy (TDD)

### 5.1 Test Structure
```
tests/
├── unit/
│   ├── test_models.py              # Data model tests
│   ├── test_prompt_analyzer.py     # Analyzer logic tests
│   ├── test_score_strategies.py    # Strategy pattern tests
│   ├── test_lesson_manager.py      # Lesson loading tests
│   ├── test_feedback_generator.py  # Feedback generation tests
│   └── test_progress_tracker.py    # Persistence tests
├── integration/
│   ├── test_learning_coach.py      # Full workflow tests
│   ├── test_openai_client.py       # API integration tests
│   └── test_lesson_flow.py         # Lesson progression tests
├── fixtures/
│   ├── sample_prompts.json         # Test prompts
│   ├── sample_lessons.json         # Test lessons
│   └── mock_ai_responses.json      # Mocked AI responses
└── conftest.py                     # Shared fixtures
```

### 5.2 TDD Examples

#### Example 1: Testing PromptAnalyzer (RED-GREEN-REFACTOR)

**RED - Write failing test first:**
```python
def test_analyzer_detects_do_it_for_me_intent():
    """Test that analyzer identifies bad prompts"""
    # Arrange
    scorer = RubricScorer()
    analyzer = PromptAnalyzer(score_strategy=scorer)
    bad_prompt = "Write my essay about climate change"
    
    # Act
    analysis = analyzer.evaluate(bad_prompt)
    
    # Assert
    assert analysis.score.intent == PromptIntent.DO_IT_FOR_ME
    assert analysis.score.total_score < 60  # Failing score
    assert "do_it_for_me" in analysis.detected_patterns
```

**GREEN - Make it pass:**
```python
# Implement _classify_intent method in RubricScorer
# Implement _detect_patterns method in PromptAnalyzer
```

**REFACTOR - Improve code:**
```python
# Extract pattern matching to separate method
# Add more comprehensive keyword lists
# Optimize performance
```

#### Example 2: Testing Strategy Pattern (LSP)
```python
def test_strategies_are_interchangeable():
    """Test that all scorers implement interface correctly (LSP)"""
    prompts = ["Explain photosynthesis", "Do my homework"]
    
    rubric_scorer = RubricScorer()
    ai_scorer = AIScorer(mock_ai_client)
    
    for scorer in [rubric_scorer, ai_scorer]:
        for prompt in prompts:
            score = scorer.calculate_score(prompt)
            
            # All strategies must return valid PromptScore
            assert isinstance(score, PromptScore)
            assert 0 <= score.total_score <= 100
            assert isinstance(score.intent, PromptIntent)
```

#### Example 3: Testing Dependency Injection (DIP)
```python
def test_learning_coach_with_mocked_dependencies():
    """Test LearningCoach works with any implementations (DIP)"""
    # Arrange - Create mocks for all dependencies
    mock_evaluator = Mock(spec=IPromptEvaluator)
    mock_lessons = Mock(spec=ILessonProvider)
    mock_feedback = Mock(spec=IFeedbackProvider)
    mock_persister = Mock(spec=IProgressPersister)
    mock_ai = Mock(spec=IAIClient)
    config = CoachConfig(api_key="test")
    
    # Mock returns
    mock_persister.load.return_value = UserProgress(
        user_id="test_user",
        current_lesson=1,
        completed_lessons=[],
        prompt_history=[],
        skill_level=1,
        total_prompts=0,
        good_prompts=0
    )
    
    # Act
    coach = LearningCoach(
        mock_evaluator, mock_lessons, mock_feedback,
        mock_persister, mock_ai, config
    )
    coach.start_session("test_user")
    
    # Assert
    mock_persister.load.assert_called_once_with("test_user")
    assert coach.current_user is not None
```

---

## 6. File Structure

```
ai_learning_coach/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── prompt_models.py
│   │   ├── lesson_models.py
│   │   └── config_models.py
│   ├── interfaces/
│   │   ├── __init__.py
│   │   └── service_interfaces.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── prompt_analyzer.py
│   │   ├── score_strategies.py
│   │   ├── lesson_manager.py
│   │   └── feedback_generator.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── openai_client.py
│   │   └── progress_persister.py
│   ├── learning_coach.py
│   ├── cli.py
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── fixtures/
│   └── conftest.py
├── data/
│   ├── lessons/
│   │   ├── lesson_01_basics.json
│   │   ├── lesson_02_specificity.json
│   │   └── lesson_03_engagement.json
│   ├── progress/
│   └── patterns/
│       └── anti_patterns.json
├── docs/
│   ├── architecture.md (this file)
│   ├── SOLID_PRINCIPLES.md
│   ├── TDD_WORKFLOW.md
│   └── USER_GUIDE.md
├── .env
├── .env.example
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 7. Example Lesson Content

### Lesson 1: The Difference Between Asking and Learning

```json
{
  "id": "lesson_01",
  "title": "Do It For Me vs Help Me Learn",
  "description": "Learn the fundamental difference between prompts that ask AI to do work vs prompts that use AI as a learning tool",
  "difficulty": 1,
  "learning_objectives": [
    "Identify 'do it for me' prompts",
    "Transform task requests into learning requests",
    "Understand why learning-focused prompts are more valuable"
  ],
  "content": "...",
  "exercises": [
    {
      "id": "ex_01_01",
      "prompt": "Transform this bad prompt into a good one",
      "expected_intent": "help_me_learn",
      "bad_example": "Write a Python function to sort a list",
      "good_example": "Explain how sorting algorithms work, then help me implement one step-by-step with hints",
      "hints": [
        "Focus on understanding, not just getting the code",
        "Ask for explanation first, then guided practice",
        "Request that AI check your understanding"
      ]
    }
  ]
}
```

---

## 8. CLI Interface Design

```bash
# Start interactive session
$ python -m src.main practice

👋 Welcome to AI Learning Coach!
📚 Learn to prompt AI effectively for learning

Choose an option:
1. Practice prompt writing
2. Take a lesson
3. View progress
4. Quick tips
5. Exit

> 1

💭 Write a prompt to ask AI about any topic:
> Write my essay about machine learning

🔍 Analyzing your prompt...

═══════════════════════════════════════════════════════════
PROMPT ANALYSIS
═══════════════════════════════════════════════════════════

Your Prompt: "Write my essay about machine learning"

Score: 25.0/100
❌ NEEDS IMPROVEMENT - Let's make this better

────────────────────────────────────────────────────────────
BREAKDOWN:
  Learning Orientation: 20.0/100
  Specificity:          30.0/100
  Engagement:           25.0/100
  Intent:               do_it_for_me

────────────────────────────────────────────────────────────
💡 HOW TO IMPROVE:
  • Focus on learning, not just getting answers. Try: 'Explain X and quiz me' instead of 'Tell me X'
  • Avoid asking AI to do your work. Ask it to teach you how to do it yourself

────────────────────────────────────────────────────────────
⚠️  ANTI-PATTERNS DETECTED:
  ⚠  do_it_for_me

────────────────────────────────────────────────────────────
📚 BETTER ALTERNATIVES:
  1. "Explain the key concepts of machine learning using simple analogies, then quiz me to check my understanding"
  2. "Help me create an outline for an essay about machine learning by asking me questions about what I already know"
  3. "What are the main topics I should cover in an essay about machine learning? After explaining each, ask if I understand before moving on"

═══════════════════════════════════════════════════════════

Try again? (y/n) >
```

---

## 9. Success Metrics

### 9.1 Technical Metrics
- ✅ 90%+ test coverage
- ✅ All SOLID principles demonstrated
- ✅ Zero circular dependencies
- ✅ <10 cyclomatic complexity per method
- ✅ Type hints on all public APIs

### 9.2 Educational Metrics
- Users can identify bad vs good prompts
- Users score 80%+ on final assessment
- Users create learning-focused prompts consistently
- Users report increased confidence in AI usage

---

## 10. Future Enhancements

### 10.1 Phase 2 Features
- **Prompt Library**: Save and share good prompts
- **Comparative Analysis**: Show before/after prompt improvements
- **AI Conversation Mode**: Practice multi-turn learning conversations
- **Peer Review**: Compare prompts with other learners
- **Badges/Achievements**: Gamification elements

### 10.2 Advanced Features
- **Domain-Specific Lessons**: Programming, writing, math, etc.
- **Voice Interface**: Practice verbal prompting
- **Integration**: Browser extension for real-time feedback
- **Analytics Dashboard**: Visualize learning progress
- **Multi-language Support**: Learn prompting in different languages

---

## 11. Conclusion

This architecture demonstrates SOLID principles in action:

- **SRP**: Each class has one clear responsibility
- **OCP**: Strategies and providers can be extended
- **LSP**: All implementations properly substitute their interfaces
- **ISP**: Focused, minimal interfaces
- **DIP**: High-level modules depend on abstractions

The TDD approach ensures quality through:
- Writing tests before implementation
- High code coverage
- Confidence in refactoring
- Living documentation

Most importantly, this project **teaches by doing** - users learn proper AI prompting by getting real-time feedback on their prompts, just as they'll learn SOLID principles by reading well-structured code.
