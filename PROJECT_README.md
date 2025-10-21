# AI Learning Coach - SOLID Design & TDD Project

> **Teach users effective AI prompting while demonstrating SOLID principles and Test-Driven Development**

[![Python](https://img.shields.io/badge/Python-3.11+-blue)]()
[![TDD](https://img.shields.io/badge/methodology-TDD-orange)]()
[![SOLID](https://img.shields.io/badge/design-SOLID-green)]()

---

## 🎯 Project Overview

**The Problem:** Many students use AI tools ineffectively, asking AI to "do their work" instead of using AI to "help them learn."

**The Solution:** An interactive CLI application that:
1. Analyzes user prompts for learning effectiveness
2. Provides constructive feedback on prompt quality
3. Teaches effective prompting through guided lessons
4. Tracks progress and encourages improvement

**The Learning Goal:** Demonstrate SOLID principles and TDD methodology through a real, useful application.

---

## 🏗️ Architecture Highlights

This project showcases **all five SOLID principles**:

### Single Responsibility Principle (SRP)
- `PromptAnalyzer` → Only analyzes prompts
- `FeedbackGenerator` → Only generates feedback
- `LessonManager` → Only manages lessons
- `ProgressPersister` → Only saves/loads data

### Open/Closed Principle (OCP)
- **Score Strategies**: Add new scoring algorithms without modifying analyzer
  ```python
  class RubricScorer(IScoreStrategy): ...
  class AIScorer(IScoreStrategy): ...
  class CustomScorer(IScoreStrategy): ...  # Easy to add!
  ```

### Liskov Substitution Principle (LSP)
- All `IScoreStrategy` implementations are interchangeable
- Tests verify substitutability

### Interface Segregation Principle (ISP)
- Small, focused interfaces
- `IPromptEvaluator`, `IScoreStrategy`, `IFeedbackProvider` each have 1-2 methods

### Dependency Inversion Principle (DIP)
- `LearningCoach` depends on interfaces, not concrete implementations
- All dependencies injected via constructor
- Easy to test, swap, and mock

---

## 📚 Documentation

### Core Documents
- **[Architecture Document](docs/AI_LEARNING_COACH_ARCHITECTURE.md)** - Complete system design (11 sections, 60+ pages)
- **[Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md)** - 10-session TDD workflow
- **[SOLID Principles Guide](docs/SOLID_PRINCIPLES_GUIDE.md)** - Detailed explanations with examples

### Quick Links
- Architecture Overview → Section 3
- SOLID Examples → Section 2
- Testing Strategy → Section 5
- TDD Workflow → Implementation Roadmap

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key (add to `.env`)

### Setup (5 minutes)
```bash
# Clone repository
git clone <your-repo-url>
cd broken_by_design

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run tests
pytest --cov=src

# Run application (once implemented)
python -m src.main practice
```

---

## 🧪 Test-Driven Development Workflow

This project follows strict TDD methodology:

### The TDD Cycle
```
1. RED   → Write failing test
2. GREEN → Write minimal code to pass
3. REFACTOR → Improve code quality
4. REPEAT
```

### Example: Building the Prompt Analyzer

**Step 1: RED - Write failing test**
```python
def test_analyzer_detects_bad_prompt():
    scorer = RubricScorer()
    analyzer = PromptAnalyzer(score_strategy=scorer)
    
    bad_prompt = "Write my essay for me"
    analysis = analyzer.evaluate(bad_prompt)
    
    assert analysis.score.total_score < 60
    assert "do_it_for_me" in analysis.detected_patterns
```

**Step 2: GREEN - Make it pass**
```python
class PromptAnalyzer:
    def evaluate(self, prompt: str) -> PromptAnalysis:
        score = self.score_strategy.calculate_score(prompt)
        patterns = self._detect_patterns(prompt)
        return PromptAnalysis(prompt, score, patterns)
```

**Step 3: REFACTOR - Improve**
```python
# Extract pattern detection
# Add comprehensive keyword lists
# Optimize performance
```

---

## 📊 Project Structure

```
ai_learning_coach/
├── src/
│   ├── models/                 # Data models (SRP)
│   │   ├── prompt_models.py
│   │   └── lesson_models.py
│   ├── interfaces/             # Abstractions (DIP, ISP)
│   │   └── service_interfaces.py
│   ├── services/               # Business logic (SRP, OCP)
│   │   ├── prompt_analyzer.py
│   │   ├── score_strategies.py
│   │   ├── lesson_manager.py
│   │   └── feedback_generator.py
│   ├── infrastructure/         # External dependencies (SRP)
│   │   ├── openai_client.py
│   │   └── progress_persister.py
│   ├── learning_coach.py       # Main orchestrator (DIP)
│   └── main.py                 # CLI entry point
├── tests/
│   ├── unit/                   # Unit tests (90%+ coverage)
│   ├── integration/            # Integration tests
│   └── fixtures/               # Test data
├── data/
│   ├── lessons/                # Lesson JSON files
│   └── progress/               # User progress data
├── docs/
│   ├── AI_LEARNING_COACH_ARCHITECTURE.md
│   ├── IMPLEMENTATION_ROADMAP.md
│   └── SOLID_PRINCIPLES_GUIDE.md
└── README.md                   # This file
```

---

## 🎓 Key Features

### 1. Prompt Analysis
```bash
$ python -m src.main practice

💭 Write a prompt: Write my Python homework

🔍 Analyzing...

Score: 25/100 ❌
Intent: do_it_for_me

💡 IMPROVEMENTS:
• Focus on learning, not just getting answers
• Try: "Explain how to solve this Python problem step-by-step"

📚 BETTER ALTERNATIVES:
1. "Teach me about Python loops with examples"
2. "Help me understand this concept, then quiz me"
```

### 2. Interactive Lessons
```bash
$ python -m src.main lesson

📚 Lesson 1: Do It For Me vs Help Me Learn

Learn to transform task requests into learning opportunities...

💪 Exercise: Improve this prompt
❌ Bad: "Write a sorting algorithm"
✅ Good: "Explain sorting algorithms, then guide me to implement one"

Your turn! >
```

### 3. Progress Tracking
```bash
$ python -m src.main progress

📊 YOUR PROGRESS
════════════════
Skill Level: 2/5
Current Lesson: 3
Total Prompts: 25
Good Prompts: 18
Success Rate: 72%
```

---

## 🧩 SOLID Principles in Practice

### Example: Strategy Pattern (OCP)

**Problem:** Different ways to score prompts (rules, AI, hybrid)

**SOLID Solution:**
```python
# Interface (abstraction)
class IScoreStrategy(ABC):
    @abstractmethod
    def calculate_score(self, prompt: str) -> PromptScore:
        pass

# Implementations (can add more without modifying existing code)
class RubricScorer(IScoreStrategy): ...
class AIScorer(IScoreStrategy): ...
class HybridScorer(IScoreStrategy): ...

# Usage (depends on abstraction, not concrete class)
analyzer = PromptAnalyzer(score_strategy=RubricScorer())
```

**Benefits:**
- ✅ Add new scorers without modifying `PromptAnalyzer`
- ✅ Easy to test (mock the strategy)
- ✅ Flexible (swap strategies at runtime)

### Example: Dependency Injection (DIP)

**Problem:** High-level orchestrator needs many components

**SOLID Solution:**
```python
class LearningCoach:
    def __init__(
        self,
        evaluator: IPromptEvaluator,     # Interface, not concrete class
        lesson_provider: ILessonProvider,
        feedback_provider: IFeedbackProvider,
        # ... all dependencies injected
    ):
        self.evaluator = evaluator
        # ...

# Production
coach = LearningCoach(
    evaluator=PromptAnalyzer(RubricScorer()),
    lesson_provider=LessonManager(),
    ...
)

# Testing (all mocked!)
coach = LearningCoach(
    evaluator=Mock(spec=IPromptEvaluator),
    lesson_provider=Mock(spec=ILessonProvider),
    ...
)
```

**Benefits:**
- ✅ Loosely coupled
- ✅ Easy to test
- ✅ Flexible configurations

---

## 📈 Development Roadmap

### Week 1: Foundation
- **Day 1**: Data models (SRP)
- **Day 2**: Interfaces & strategies (OCP, ISP)
- **Day 3**: Prompt analyzer (SRP, DIP)
- **Day 4**: Feedback generator (SRP)
- **Day 5**: Lesson manager (SRP, OCP)

### Week 2: Integration
- **Day 6**: Progress tracking (SRP, DIP)
- **Day 7**: OpenAI client (SRP)
- **Day 8**: Main orchestrator (DIP)
- **Day 9**: CLI interface
- **Day 10**: Integration tests & polish

**See [Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md) for detailed TDD workflow**

---

## ✅ Success Criteria

### Technical Requirements
- [ ] 90%+ test coverage
- [ ] All SOLID principles demonstrated
- [ ] Zero circular dependencies
- [ ] Type hints on all public APIs
- [ ] Passing linter checks

### Functional Requirements
- [ ] Analyze prompts and provide scores
- [ ] Detect anti-patterns (e.g., "do_it_for_me")
- [ ] Generate constructive feedback
- [ ] Teach lessons interactively
- [ ] Track and persist user progress

### Educational Requirements
- [ ] Code demonstrates SOLID clearly
- [ ] Tests show TDD workflow
- [ ] Documentation explains design decisions
- [ ] Application actually teaches effective prompting

---

## 🎯 Learning Outcomes

After completing this project, you will:

✅ **Understand SOLID principles** through real implementation  
✅ **Master TDD methodology** with practical examples  
✅ **Build testable, maintainable code** using design patterns  
✅ **Work with AI APIs** effectively  
✅ **Design clean architectures** with proper separation of concerns  
✅ **Write comprehensive tests** with high coverage  
✅ **Use dependency injection** for flexibility  
✅ **Apply interface-based design** for extensibility  

---

## 🤝 Contributing

This is an educational project. Focus on:
- Following SOLID principles
- Writing tests first (TDD)
- Clear, documented code
- Meaningful commit messages

---

## 📖 Additional Resources

### SOLID Principles
- [SOLID Principles Guide](docs/SOLID_PRINCIPLES_GUIDE.md) - Detailed explanations with project examples
- [Architecture Document](docs/AI_LEARNING_COACH_ARCHITECTURE.md) - Section 2: SOLID Application

### Test-Driven Development
- [Implementation Roadmap](docs/IMPLEMENTATION_ROADMAP.md) - Session-by-session TDD workflow
- [Architecture Document](docs/AI_LEARNING_COACH_ARCHITECTURE.md) - Section 5: Testing Strategy

### Design Patterns
- Strategy Pattern → `score_strategies.py`
- Dependency Injection → `learning_coach.py`
- Interface Segregation → `interfaces/service_interfaces.py`

---

## 🚀 Next Steps

1. **Read the Architecture Document** - Understand the system design
2. **Review SOLID Principles Guide** - See examples in context
3. **Follow Implementation Roadmap** - Build it step-by-step with TDD
4. **Run Tests Frequently** - Maintain high coverage
5. **Refactor Continuously** - Keep code clean

**Start with:** [Architecture Document](docs/AI_LEARNING_COACH_ARCHITECTURE.md) Section 1-3

---

## 📝 License

Educational project for learning SOLID principles and TDD.

---

<div align="center">

**Let's build something that demonstrates excellent design! 🚀**

*Because the best way to learn SOLID is to see it in action*

</div>
