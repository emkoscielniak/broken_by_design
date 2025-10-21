# AI Learning Coach - TDD Implementation Roadmap

**Goal:** Build the AI Learning Coach following Test-Driven Development

**Timeline:** 2-week sprint (10 sessions)

---

## Week 1: Foundation & Core Components

### Session 1: Project Setup & Models (Day 1)
**Duration:** 90 minutes

**TDD Cycle 1: Data Models**
```python
# RED: Write test first
def test_prompt_score_creation():
    score = PromptScore(
        total_score=75.0,
        learning_orientation=80.0,
        specificity=70.0,
        engagement=75.0,
        intent=PromptIntent.HELP_ME_LEARN
    )
    assert score.is_passing == True
    assert score.total_score == 75.0

# GREEN: Implement PromptScore
# REFACTOR: Add validation
```

**Tasks:**
- [ ] Create project structure
- [ ] Write tests for `PromptScore` model
- [ ] Implement `PromptScore` with `is_passing` property
- [ ] Write tests for `PromptIntent` enum
- [ ] Write tests for `PromptAnalysis` model
- [ ] Implement `PromptAnalysis`
- [ ] Write tests for `Lesson` and `Exercise` models
- [ ] Implement lesson models
- [ ] Achieve 100% coverage on models

**Deliverable:** All data models with passing tests

---

### Session 2: Interfaces & Strategy Pattern (Day 2)
**Duration:** 90 minutes

**TDD Cycle 2: Score Strategies**
```python
# RED: Write interface tests
def test_rubric_scorer_implements_interface():
    scorer = RubricScorer()
    assert isinstance(scorer, IScoreStrategy)
    
def test_rubric_scorer_calculates_score():
    scorer = RubricScorer()
    score = scorer.calculate_score("Explain photosynthesis and quiz me")
    assert isinstance(score, PromptScore)
    assert score.total_score > 0

# GREEN: Implement RubricScorer
# REFACTOR: Extract common scoring logic
```

**Tasks:**
- [ ] Define all interfaces in `src/interfaces/`
- [ ] Write tests for `IScoreStrategy` interface
- [ ] Implement `RubricScorer` (rule-based)
- [ ] Write tests for learning orientation scoring
- [ ] Write tests for specificity scoring
- [ ] Write tests for engagement scoring
- [ ] Write tests for intent classification
- [ ] Verify LSP with multiple strategies
- [ ] Achieve 100% coverage on scorer

**Deliverable:** Working RubricScorer with comprehensive tests

---

### Session 3: Prompt Analyzer (Day 3)
**Duration:** 90 minutes

**TDD Cycle 3: Analyzer Logic**
```python
# RED: Write analyzer tests
def test_analyzer_evaluates_good_prompt():
    scorer = RubricScorer()
    analyzer = PromptAnalyzer(score_strategy=scorer)
    
    good_prompt = "Explain Python decorators with examples, then give me practice exercises"
    analysis = analyzer.evaluate(good_prompt)
    
    assert analysis.score.is_passing
    assert len(analysis.strengths) > 0
    assert analysis.score.intent == PromptIntent.HELP_ME_LEARN

def test_analyzer_detects_anti_patterns():
    scorer = RubricScorer()
    analyzer = PromptAnalyzer(score_strategy=scorer)
    
    bad_prompt = "Write my code for me"
    analysis = analyzer.evaluate(bad_prompt)
    
    assert "do_it_for_me" in analysis.detected_patterns
    assert len(analysis.improvements) > 0

# GREEN: Implement PromptAnalyzer
# REFACTOR: Extract pattern detection
```

**Tasks:**
- [ ] Write tests for `PromptAnalyzer.__init__`
- [ ] Write tests for `evaluate()` method
- [ ] Implement basic evaluation flow
- [ ] Write tests for pattern detection
- [ ] Implement anti-pattern matching
- [ ] Write tests for strength identification
- [ ] Implement strength detection
- [ ] Write tests for improvement suggestions
- [ ] Implement improvement logic
- [ ] Verify DIP (works with any IScoreStrategy)
- [ ] Achieve 100% coverage on analyzer

**Deliverable:** Full PromptAnalyzer with pattern detection

---

### Session 4: Feedback Generator (Day 4)
**Duration:** 90 minutes

**TDD Cycle 4: Feedback Formatting**
```python
# RED: Write feedback tests
def test_detailed_feedback_format():
    analysis = create_sample_analysis()  # Fixture
    generator = FeedbackGenerator(style="detailed")
    
    feedback = generator.generate_feedback(analysis)
    
    assert "PROMPT ANALYSIS" in feedback
    assert "Score:" in feedback
    assert "STRENGTHS:" in feedback
    assert "HOW TO IMPROVE:" in feedback

def test_concise_feedback_format():
    analysis = create_sample_analysis()
    generator = FeedbackGenerator(style="concise")
    
    feedback = generator.generate_feedback(analysis)
    
    assert len(feedback) < 200  # Brief
    assert "✅" in feedback or "❌" in feedback

# GREEN: Implement FeedbackGenerator
# REFACTOR: Extract formatting helpers
```

**Tasks:**
- [ ] Write tests for `FeedbackGenerator.__init__`
- [ ] Write tests for detailed feedback format
- [ ] Implement `_detailed_feedback()`
- [ ] Write tests for concise feedback format
- [ ] Implement `_concise_feedback()`
- [ ] Write tests for beginner feedback format
- [ ] Implement `_beginner_feedback()`
- [ ] Verify OCP (can add new styles easily)
- [ ] Achieve 100% coverage on generator

**Deliverable:** Feedback generator with multiple styles

---

### Session 5: Lesson Manager (Day 5)
**Duration:** 90 minutes

**TDD Cycle 5: Lesson Loading**
```python
# RED: Write lesson manager tests
def test_lesson_manager_loads_lessons():
    manager = LessonManager("tests/fixtures/lessons")
    lessons = manager.get_lessons_by_level(1)
    
    assert len(lessons) > 0
    assert all(lesson.difficulty == 1 for lesson in lessons)

def test_lesson_manager_gets_specific_lesson():
    manager = LessonManager("tests/fixtures/lessons")
    lesson = manager.get_lesson("lesson_01")
    
    assert lesson.id == "lesson_01"
    assert lesson.title is not None

def test_lesson_manager_handles_missing_lesson():
    manager = LessonManager("tests/fixtures/lessons")
    
    with pytest.raises(ValueError):
        manager.get_lesson("nonexistent")

# GREEN: Implement LessonManager
# REFACTOR: Extract JSON parsing
```

**Tasks:**
- [ ] Create sample lesson JSON fixtures
- [ ] Write tests for lesson loading
- [ ] Implement `_load_all_lessons()`
- [ ] Write tests for `get_lesson()`
- [ ] Implement lesson retrieval
- [ ] Write tests for `get_lessons_by_level()`
- [ ] Implement level filtering
- [ ] Write tests for error handling
- [ ] Implement robust error messages
- [ ] Achieve 100% coverage on manager

**Deliverable:** Lesson manager with JSON loading

---

## Week 2: Integration & Polish

### Session 6: Progress Tracking (Day 6)
**Duration:** 90 minutes

**TDD Cycle 6: Persistence**
```python
# RED: Write persister tests
def test_save_and_load_progress(tmp_path):
    persister = JSONProgressPersister(str(tmp_path))
    
    progress = UserProgress(
        user_id="test_user",
        current_lesson=3,
        completed_lessons=["lesson_01", "lesson_02"],
        prompt_history=[],
        skill_level=2,
        total_prompts=10,
        good_prompts=8
    )
    
    persister.save(progress)
    loaded = persister.load("test_user")
    
    assert loaded.user_id == "test_user"
    assert loaded.current_lesson == 3
    assert loaded.good_prompts == 8

# GREEN: Implement JSONProgressPersister
# REFACTOR: Add validation
```

**Tasks:**
- [ ] Write tests for `save()` method
- [ ] Implement progress serialization
- [ ] Write tests for `load()` method
- [ ] Implement progress deserialization
- [ ] Write tests for new user creation
- [ ] Implement default progress
- [ ] Write tests for file handling errors
- [ ] Implement error handling
- [ ] Verify DIP (interface-based)
- [ ] Achieve 100% coverage on persister

**Deliverable:** Working progress persistence

---

### Session 7: OpenAI Client (Day 7)
**Duration:** 90 minutes

**TDD Cycle 7: API Integration**
```python
# RED: Write client tests (with mocks)
def test_openai_client_chat(mock_openai):
    client = OpenAIClient(api_key="test-key")
    
    messages = [{"role": "user", "content": "Hello"}]
    response = client.chat(messages)
    
    assert isinstance(response, str)
    assert len(response) > 0

def test_openai_client_analyze_prompt(mock_openai):
    client = OpenAIClient(api_key="test-key")
    
    result = client.analyze_prompt_intent("Explain Python")
    
    assert "total_score" in result
    assert "intent" in result

# GREEN: Implement OpenAIClient
# REFACTOR: Add retry logic
```

**Tasks:**
- [ ] Write tests for `__init__` with API key
- [ ] Implement client initialization
- [ ] Write tests for `chat()` method (mocked)
- [ ] Implement chat completion
- [ ] Write tests for `analyze_prompt_intent()`
- [ ] Implement prompt analysis
- [ ] Write tests for error handling
- [ ] Implement API error catching
- [ ] Create `AIScorer` using client
- [ ] Achieve 90%+ coverage (skip live API)

**Deliverable:** OpenAI client with mocked tests

---

### Session 8: Learning Coach Orchestrator (Day 8)
**Duration:** 90 minutes

**TDD Cycle 8: Main Application**
```python
# RED: Write orchestrator tests
def test_learning_coach_initialization(mock_deps):
    coach = LearningCoach(**mock_deps)
    
    assert coach.evaluator is not None
    assert coach.lesson_provider is not None

def test_learning_coach_starts_session(mock_deps):
    coach = LearningCoach(**mock_deps)
    coach.start_session("user_123")
    
    assert coach.current_user is not None
    assert coach.current_user.user_id == "user_123"

def test_learning_coach_practice_prompt(mock_deps):
    coach = LearningCoach(**mock_deps)
    coach.start_session("user_123")
    
    initial_count = coach.current_user.total_prompts
    coach.practice_prompt("Explain recursion")
    
    assert coach.current_user.total_prompts == initial_count + 1

# GREEN: Implement LearningCoach
# REFACTOR: Extract session logic
```

**Tasks:**
- [ ] Write tests for DI constructor
- [ ] Implement `__init__` with all dependencies
- [ ] Write tests for `start_session()`
- [ ] Implement session initialization
- [ ] Write tests for `practice_prompt()`
- [ ] Implement prompt evaluation flow
- [ ] Write tests for `teach_lesson()`
- [ ] Implement lesson display
- [ ] Write tests for progress updates
- [ ] Implement auto-advancement logic
- [ ] Verify SOLID principles
- [ ] Achieve 100% coverage on coach

**Deliverable:** Full LearningCoach orchestrator

---

### Session 9: CLI Interface (Day 9)
**Duration:** 90 minutes

**TDD Cycle 9: User Interface**
```python
# RED: Write CLI tests
def test_cli_parse_arguments():
    args = parse_args(["practice"])
    assert args.command == "practice"

def test_cli_practice_mode(mock_coach, monkeypatch):
    # Mock user input
    inputs = iter(["Explain Python", "n"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    run_practice_mode(mock_coach)
    
    # Verify coach.practice_prompt was called

# GREEN: Implement CLI
# REFACTOR: Extract display functions
```

**Tasks:**
- [ ] Write tests for argument parsing
- [ ] Implement CLI argument parser
- [ ] Write tests for practice mode
- [ ] Implement interactive practice
- [ ] Write tests for lesson mode
- [ ] Implement lesson teaching flow
- [ ] Write tests for progress display
- [ ] Implement progress report
- [ ] Write tests for main() function
- [ ] Implement main entry point
- [ ] Achieve 90%+ coverage on CLI

**Deliverable:** Full CLI interface

---

### Session 10: Integration Tests & Documentation (Day 10)
**Duration:** 90 minutes

**Integration Testing**
```python
# Integration: Full workflow test
def test_complete_learning_session(tmp_path):
    # Setup real components (no mocks)
    scorer = RubricScorer()
    analyzer = PromptAnalyzer(score_strategy=scorer)
    lesson_mgr = LessonManager("data/lessons")
    feedback_gen = FeedbackGenerator(style="detailed")
    persister = JSONProgressPersister(str(tmp_path))
    mock_ai = MockAIClient()  # Mock only external API
    config = CoachConfig(api_key="test")
    
    coach = LearningCoach(
        analyzer, lesson_mgr, feedback_gen,
        persister, mock_ai, config
    )
    
    # Run full session
    coach.start_session("integration_test_user")
    coach.practice_prompt("Explain decorators and quiz me")
    coach.practice_prompt("Write my code")  # Bad prompt
    coach.show_progress_report()
    coach.end_session()
    
    # Verify end-to-end behavior
    loaded = persister.load("integration_test_user")
    assert loaded.total_prompts == 2
    assert loaded.good_prompts == 1

# Test with real lessons
# Test with real OpenAI (optional, marked)
```

**Tasks:**
- [ ] Write end-to-end integration tests
- [ ] Run full test suite
- [ ] Verify 90%+ total coverage
- [ ] Create sample lesson files
- [ ] Write README.md
- [ ] Document SOLID principles used
- [ ] Create user guide
- [ ] Add inline code documentation
- [ ] Final refactoring pass
- [ ] Code quality check (pylint)

**Deliverable:** Fully tested, documented application

---

## Test Coverage Goals

| Component | Target Coverage | Priority |
|-----------|----------------|----------|
| Models | 100% | High |
| PromptAnalyzer | 100% | High |
| ScoreStrategies | 100% | High |
| FeedbackGenerator | 100% | High |
| LessonManager | 100% | High |
| ProgressPersister | 100% | High |
| LearningCoach | 100% | High |
| OpenAIClient | 90% | Medium (mock API) |
| CLI | 90% | Medium (I/O heavy) |
| Integration | 80% | Medium |

---

## SOLID Principles Checklist

### Single Responsibility Principle (SRP)
- [ ] PromptAnalyzer only analyzes prompts
- [ ] FeedbackGenerator only generates feedback
- [ ] LessonManager only manages lessons
- [ ] ProgressPersister only handles persistence
- [ ] OpenAIClient only communicates with API

### Open/Closed Principle (OCP)
- [ ] Can add new ScoreStrategy without changing PromptAnalyzer
- [ ] Can add new FeedbackProvider without changing LearningCoach
- [ ] Can add new lesson types without changing LessonManager
- [ ] Can add new anti-patterns via configuration

### Liskov Substitution Principle (LSP)
- [ ] RubricScorer and AIScorer are interchangeable
- [ ] All IPromptEvaluator implementations work identically
- [ ] All IProgressPersister implementations work identically

### Interface Segregation Principle (ISP)
- [ ] IScoreStrategy has minimal interface (just calculate_score)
- [ ] ILessonProvider has focused lesson operations
- [ ] IFeedbackProvider has single responsibility
- [ ] No fat interfaces

### Dependency Inversion Principle (DIP)
- [ ] LearningCoach depends on interfaces, not implementations
- [ ] PromptAnalyzer depends on IScoreStrategy interface
- [ ] High-level modules don't know about low-level details
- [ ] All dependencies injected via constructor

---

## Success Criteria

### Functional Requirements
- ✅ Analyze prompts and provide scores
- ✅ Detect anti-patterns
- ✅ Generate constructive feedback
- ✅ Teach lessons interactively
- ✅ Track user progress
- ✅ Save and load user data

### Non-Functional Requirements
- ✅ 90%+ test coverage
- ✅ All SOLID principles demonstrated
- ✅ TDD methodology followed
- ✅ Clean, documented code
- ✅ Type hints on all public APIs
- ✅ No circular dependencies

### Educational Requirements
- ✅ Code demonstrates SOLID clearly
- ✅ Tests show TDD workflow
- ✅ Application teaches effective prompting
- ✅ Documentation explains design decisions

---

## Daily Workflow

Each session follows this pattern:

1. **Review** (5 min)
   - Review previous session's work
   - Check test coverage
   - Verify no regressions

2. **RED** (25 min)
   - Write failing tests for new feature
   - Run tests, confirm they fail
   - Think through edge cases

3. **GREEN** (35 min)
   - Write minimal code to pass tests
   - Run tests frequently
   - Don't over-engineer

4. **REFACTOR** (20 min)
   - Improve code quality
   - Extract methods
   - Verify SOLID principles
   - Ensure tests still pass

5. **Commit** (5 min)
   - Write meaningful commit message
   - Push to repository
   - Update roadmap checklist

---

## Git Workflow

```bash
# Day 1
git checkout -b feature/data-models
# ... TDD work ...
git add .
git commit -m "feat: implement data models with 100% coverage"
git push origin feature/data-models

# Day 2
git checkout -b feature/score-strategies
# ... TDD work ...
git commit -m "feat: implement RubricScorer with strategy pattern"
git push origin feature/score-strategies

# Continue for each feature...
```

---

## Resources Needed

### Development
- Python 3.11+
- pytest, pytest-cov, pytest-mock
- OpenAI API key
- VS Code or PyCharm

### Documentation
- Architecture diagram tools (draw.io)
- Markdown editor
- Code documentation generator

### Sample Data
- Anti-pattern definitions
- Lesson JSON files
- Example prompts (good and bad)

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| OpenAI API costs | Use mocks for most tests, limit live API calls |
| Scope creep | Stick to roadmap, track "nice to have" separately |
| Test complexity | Keep tests simple, use fixtures for reuse |
| Time overruns | Prioritize core features, defer enhancements |
| SOLID violations | Regular code reviews, refactoring sessions |

---

## Conclusion

By following this roadmap, you'll build a production-quality application that:

1. **Demonstrates SOLID principles** in every component
2. **Uses TDD methodology** throughout development
3. **Teaches effective AI prompting** to users
4. **Maintains high code quality** with comprehensive tests

Most importantly, you'll learn by doing - experiencing firsthand how SOLID and TDD lead to maintainable, testable, extensible code.

**Next Step:** Start Session 1 - Write your first test!
