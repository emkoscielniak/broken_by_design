# AI Learning Coach - Visual Architecture Summary

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERACTION                            │
│                         (CLI Interface)                              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       LEARNING COACH                                 │
│                    (Main Orchestrator)                               │
│                                                                       │
│  Responsibilities:                                                   │
│  • Coordinate learning flow                                          │
│  • Manage user sessions                                              │
│  • Update progress                                                   │
│                                                                       │
│  SOLID Principles:                                                   │
│  • SRP: Only orchestrates, doesn't implement details                │
│  • DIP: Depends on interfaces (all dependencies injected)           │
└──┬──────────┬──────────┬──────────┬──────────┬─────────────────────┘
   │          │          │          │          │
   │          │          │          │          │
   ▼          ▼          ▼          ▼          ▼
┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
│Eval │  │Less │  │Feed │  │Prog │  │AI   │
│uator│  │on   │  │back │  │ress │  │Clien│
│     │  │Mgr  │  │Gen  │  │Track│  │t    │
└─────┘  └─────┘  └─────┘  └─────┘  └─────┘
```

---

## SOLID Principles Visualization

### 1. Single Responsibility Principle (SRP)

```
Each box has ONE job:

┌──────────────┐
│PromptAnalyzer│  → Only analyzes prompts
└──────────────┘

┌──────────────┐
│FeedbackGen   │  → Only generates feedback
└──────────────┘

┌──────────────┐
│LessonManager │  → Only manages lessons
└──────────────┘

┌──────────────┐
│ProgressTrack│  → Only tracks progress
└──────────────┘

┌──────────────┐
│OpenAIClient  │  → Only calls API
└──────────────┘
```

### 2. Open/Closed Principle (OCP)

```
Open for extension, closed for modification:

                ┌──────────────┐
                │IScoreStrategy│  (Interface)
                └───────┬──────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│RubricScorer  │ │AIScorer  │ │HybridScorer  │
└──────────────┘ └──────────┘ └──────────────┘

Want to add new scorer?
        │
        ▼
┌──────────────┐
│CustomScorer  │  ← Just implement interface!
└──────────────┘    No need to modify existing code
```

### 3. Liskov Substitution Principle (LSP)

```
All implementations are substitutable:

┌──────────────────────────────────────┐
│PromptAnalyzer(strategy: IScoreStrategy)│
└──────────────────────────────────────┘
              ↑
              │
    All these work identically:
              │
    ┌─────────┴─────────┐
    │                   │
    ▼                   ▼
RubricScorer        AIScorer
    │                   │
    └─────────┬─────────┘
              │
              ▼
        HybridScorer

Any IScoreStrategy can be used without breaking the analyzer!
```

### 4. Interface Segregation Principle (ISP)

```
Small, focused interfaces:

❌ FAT INTERFACE (Don't do this):
┌────────────────────────────┐
│ILearningSystem             │
│ • score_prompt()           │
│ • generate_feedback()      │
│ • load_lessons()           │
│ • save_progress()          │
│ • call_ai_api()            │
└────────────────────────────┘
   Too many responsibilities!


✅ FOCUSED INTERFACES (Do this):
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│IScoreStrategy│  │IFeedbackProv │  │ILessonProvider│
│              │  │              │  │              │
│• calc_score()│  │• generate()  │  │• get_lesson()│
└──────────────┘  └──────────────┘  └──────────────┘
   One purpose       One purpose       One purpose
```

### 5. Dependency Inversion Principle (DIP)

```
Depend on abstractions, not concretions:

HIGH-LEVEL MODULE:
┌──────────────────────────────────┐
│     LearningCoach                │
│                                  │
│  def __init__(                   │
│    evaluator: IPromptEvaluator   │  ← Interface (abstraction)
│    lessons: ILessonProvider      │  ← Interface (abstraction)
│    feedback: IFeedbackProvider   │  ← Interface (abstraction)
│    ...                           │
│  )                               │
└──────────────────────────────────┘
                │
                │ Depends on abstractions
                │
                ▼
┌─────────────────────────────────────┐
│         INTERFACES                  │
│  (Abstractions, not implementations)│
└──────────────┬──────────────────────┘
               │
               │ Implemented by
               │
               ▼
┌─────────────────────────────────────┐
│     LOW-LEVEL MODULES               │
│  PromptAnalyzer, LessonManager, etc │
└─────────────────────────────────────┘
```

---

## Data Flow

### Prompt Analysis Flow

```
1. User enters prompt
   │
   ▼
2. LearningCoach receives it
   │
   ▼
3. Calls evaluator.evaluate(prompt)
   │
   ▼
4. PromptAnalyzer:
   │
   ├─→ Calls score_strategy.calculate_score()
   │   │
   │   └─→ RubricScorer/AIScorer calculates score
   │
   ├─→ Detects anti-patterns
   │
   ├─→ Identifies strengths
   │
   └─→ Suggests improvements
   │
   ▼
5. Returns PromptAnalysis object
   │
   ▼
6. LearningCoach passes to feedback_provider
   │
   ▼
7. FeedbackGenerator formats for display
   │
   ▼
8. Display to user
   │
   ▼
9. Save to progress_persister
```

### Lesson Flow

```
1. User selects lesson
   │
   ▼
2. LearningCoach calls lesson_provider.get_lesson()
   │
   ▼
3. LessonManager loads from JSON
   │
   ▼
4. Returns Lesson object
   │
   ▼
5. LearningCoach displays lesson content
   │
   ▼
6. User completes exercises
   │
   ▼
7. Each exercise prompt evaluated (see above)
   │
   ▼
8. Progress updated
```

---

## Test Strategy

### Test Pyramid

```
                    ▲
                   ╱ ╲
                  ╱   ╲
                 ╱     ╲
                ╱       ╲
               ╱  E2E    ╲         Few, slow, high-level
              ╱           ╲
             ╱─────────────╲
            ╱               ╲
           ╱  Integration    ╲    Some, medium speed
          ╱                   ╲
         ╱─────────────────────╲
        ╱                       ╲
       ╱        Unit Tests       ╲  Many, fast, focused
      ╱                           ╲
     ╱─────────────────────────────╲
    ╱                               ╲
   ╱_________________________________╲
```

### TDD Cycle

```
┌─────────────┐
│    RED      │  Write failing test
│   ❌ Test   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   GREEN     │  Write minimal code to pass
│   ✅ Test   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  REFACTOR   │  Improve code quality
│  ♻️  Code    │
└──────┬──────┘
       │
       └──────► REPEAT
```

---

## Component Dependencies

### Dependency Graph (DIP)

```
LearningCoach (depends on interfaces only)
    │
    ├─→ IPromptEvaluator
    │       └─→ PromptAnalyzer (implementation)
    │               └─→ IScoreStrategy
    │                       ├─→ RubricScorer
    │                       └─→ AIScorer
    │
    ├─→ ILessonProvider
    │       └─→ LessonManager (implementation)
    │
    ├─→ IFeedbackProvider
    │       └─→ FeedbackGenerator (implementation)
    │
    ├─→ IProgressPersister
    │       └─→ JSONProgressPersister (implementation)
    │
    └─→ IAIClient
            └─→ OpenAIClient (implementation)

Notice: LearningCoach knows NOTHING about concrete implementations!
```

---

## Example User Session

```
┌────────────────────────────────────────────────────────────┐
│  $ python -m src.main practice                             │
└────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────┐
│  👋 Welcome to AI Learning Coach!                          │
│  📊 Your stats: 18/25 good prompts (72%)                   │
└────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────┐
│  💭 Write a prompt:                                         │
│  > Write my essay about climate change                     │
└────────────────────────────────────────────────────────────┘
                          │
                          ▼
         [PromptAnalyzer evaluates prompt]
                          │
                          ▼
┌────────────────────────────────────────────────────────────┐
│  🔍 ANALYSIS                                                │
│  Score: 25/100 ❌                                           │
│  Intent: do_it_for_me                                      │
│                                                             │
│  ⚠️  ANTI-PATTERNS:                                         │
│  • Asking AI to do work instead of teaching                │
│                                                             │
│  💡 IMPROVEMENTS:                                           │
│  • Focus on learning, not just getting answers             │
│  • Ask AI to explain concepts and quiz you                 │
│                                                             │
│  📚 BETTER ALTERNATIVES:                                    │
│  1. "Explain climate change causes, then quiz me"          │
│  2. "Help me outline an essay by asking what I know"       │
└────────────────────────────────────────────────────────────┘
                          │
                          ▼
         [Progress saved to JSON file]
                          │
                          ▼
┌────────────────────────────────────────────────────────────┐
│  Try again? (y/n)                                           │
└────────────────────────────────────────────────────────────┘
```

---

## File Organization

```
src/
│
├── models/                    # Data structures (SRP)
│   ├── prompt_models.py       # PromptScore, PromptAnalysis
│   └── lesson_models.py       # Lesson, Exercise
│
├── interfaces/                # Abstractions (DIP, ISP)
│   └── service_interfaces.py  # All interfaces defined here
│
├── services/                  # Business logic (SRP, OCP)
│   ├── prompt_analyzer.py     # Analyzes prompts
│   ├── score_strategies.py    # Strategy implementations
│   ├── lesson_manager.py      # Manages lessons
│   └── feedback_generator.py  # Generates feedback
│
├── infrastructure/            # External systems (SRP)
│   ├── openai_client.py       # API communication
│   └── progress_persister.py  # Data persistence
│
├── learning_coach.py          # Main orchestrator (DIP)
└── main.py                    # CLI entry point

tests/
├── unit/                      # Fast, isolated tests
├── integration/               # Component interaction tests
└── fixtures/                  # Test data
```

---

## Key Design Decisions

### Why Strategy Pattern?
```
PROBLEM: Multiple ways to score prompts
SOLUTION: Strategy pattern (OCP)
BENEFIT: Add new scoring methods without modifying analyzer
```

### Why Dependency Injection?
```
PROBLEM: Components need to work together but stay loosely coupled
SOLUTION: Constructor injection of interfaces (DIP)
BENEFIT: Easy to test, mock, and swap implementations
```

### Why Small Interfaces?
```
PROBLEM: Large interfaces force unnecessary implementations
SOLUTION: Focused interfaces (ISP)
BENEFIT: Implement only what's needed
```

### Why Separate Classes?
```
PROBLEM: One big class is hard to test and maintain
SOLUTION: Single responsibility per class (SRP)
BENEFIT: Easy to understand, test, and modify
```

---

## Success Metrics

### Code Quality
```
┌─────────────────────────────┐
│ Test Coverage:     90%+     │
│ Cyclomatic Complexity: <10  │
│ SOLID Violations:  0        │
│ Circular Dependencies: 0    │
│ Type Hints:        100%     │
└─────────────────────────────┘
```

### Functionality
```
┌─────────────────────────────┐
│ ✅ Analyze prompts          │
│ ✅ Detect anti-patterns     │
│ ✅ Generate feedback        │
│ ✅ Teach lessons            │
│ ✅ Track progress           │
└─────────────────────────────┘
```

---

## Learning Path

```
Week 1: Foundation
├── Day 1: Models (SRP)
├── Day 2: Interfaces & Strategies (OCP, ISP)
├── Day 3: Analyzer (SRP, DIP)
├── Day 4: Feedback (SRP)
└── Day 5: Lessons (SRP, OCP)

Week 2: Integration
├── Day 6: Progress (SRP, DIP)
├── Day 7: API Client (SRP)
├── Day 8: Orchestrator (DIP)
├── Day 9: CLI
└── Day 10: Integration tests & polish

Each day: RED → GREEN → REFACTOR
```

---

## Quick Reference

### SOLID Checklist
- [ ] Each class has one responsibility (SRP)
- [ ] Can extend without modifying (OCP)
- [ ] Subtypes work like parent types (LSP)
- [ ] Interfaces are minimal (ISP)
- [ ] Depend on abstractions (DIP)

### TDD Checklist
- [ ] Write test first (RED)
- [ ] Make it pass (GREEN)
- [ ] Improve code (REFACTOR)
- [ ] Commit with meaningful message
- [ ] Repeat

---

<div align="center">

**This architecture demonstrates professional software design**

SOLID Principles + Test-Driven Development = Maintainable Code

</div>
