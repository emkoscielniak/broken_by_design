# ✸ Broken by Design

> **An AI-powered learning coach that teaches you how to prompt AI effectively**

[![Tests](https://img.shields.io/badge/tests-73%20passing-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-92.87%25-brightgreen)]()
[![TDD](https://img.shields.io/badge/methodology-TDD-orange)]()
[![SOLID](https://img.shields.io/badge/architecture-SOLID-blue)]()

---

## What This Project Does

**Broken by Design** is an interactive web application that helps users learn to craft better AI prompts through:

**Real-time Feedback** • **Structured Lessons** • **Progress Tracking** • **Multiple Learning Styles** • **OpenAI Integration**

**The Philosophy:** Most people use AI poorly—asking it to "do it for me" instead of "help me learn." This app teaches the difference through analysis, scoring, and personalized coaching.

---

## 🎯 Three Ways to Use This

<table>
<tr>
<td width="33%" align="center">
<h3>🏃‍♂️ Try the App</h3>
<p><strong>5-minute setup</strong></p>
<a href="#-quick-start">Launch Broken by Design →</a>
<br><br>
<em>Analyze prompts, get feedback</em>
</td>
<td width="33%" align="center">
<h3>📚 Study the Code</h3>
<p><strong>See SOLID in action</strong></p>
<a href="ai_learning_coach/src/">Browse Architecture →</a>
<br><br>
<em>Clean architecture, TDD, DI</em>
</td>
<td width="33%" align="center">
<h3>🛠️ Extend It</h3>
<p><strong>Build new features</strong></p>
<a href="#-project-structure">Explore Structure →</a>
<br><br>
<em>Add lessons, scoring, styles</em>
</td>
</tr>
</table>

---

## ✨ Key Features

### 📊 **Prompt Analysis**
- Real-time scoring across 3 dimensions: Learning Orientation, Specificity, Engagement
- AI-powered intent detection (Do It For Me vs. Help Me Learn)
- Anti-pattern detection and improvement suggestions
- Concrete examples showing better alternatives

### 📚 **Structured Lessons**
- 5 progressive lessons from beginner to advanced
- Interactive exercises with hints and examples
- Skill-based recommendations
- Progress tracking and completion badges

### 💬 **Personalized Feedback**
Choose your learning style:
- **Encouraging**: Positive, supportive coaching
- **Direct**: Straightforward, fact-based feedback
- **Socratic**: Reflective questions to guide discovery

### � **Progress Tracking**
- Track total prompts analyzed
- Monitor success rate and skill level
- Review prompt history with scores
- Optional email-based progress saving

### 🤖 **OpenAI Integration**
- Real-time chat with GPT-4o-mini
- AI-enhanced intent analysis
- Conversational feedback generation

---

## 🏗️ Project Structure

**Clean Architecture with SOLID Principles:**

```
ai_learning_coach/
├── app.py                                    → Streamlit web interface
├── src/
│   ├── models/
│   │   └── prompt_models.py                  → 8 data models with validation
│   ├── interfaces/
│   │   └── service_interfaces.py             → 6 interface contracts (ISP, DIP)
│   ├── services/
│   │   ├── score_strategies.py               → Strategy pattern for scoring
│   │   ├── prompt_analyzer.py                → Prompt evaluation service
│   │   ├── feedback_generator.py             → Multi-style feedback
│   │   └── lesson_manager.py                 → Lesson recommendations
│   └── infrastructure/
│       └── openai_client.py                  → OpenAI API integration
│
└── tests/                                     → 73 tests, 92.87% coverage
    ├── unit/
    │   ├── test_models.py                    → 22 model tests
    │   ├── test_score_strategies.py          → 14 scoring tests
    │   ├── test_prompt_analyzer.py           → 13 analyzer tests
    │   ├── test_feedback_generator.py        → 12 feedback tests
    │   └── test_lesson_manager.py            → 12 lesson tests
    └── conftest.py                           → Shared test fixtures
```

**SOLID Principles Demonstrated:**
- **SRP**: Each class has one responsibility (scorer, analyzer, generator)
- **OCP**: Strategy pattern allows new scoring algorithms without changes
- **LSP**: All strategies implement same interface correctly
- **ISP**: Small, focused interfaces (3-6 methods each)
- **DIP**: Services depend on abstractions, not concrete classes

---

## � Educational Value

**Learn Industry-Standard Practices:**

### Test-Driven Development (TDD)
- 73 tests written BEFORE implementation
- RED-GREEN-REFACTOR methodology
- 92.87% code coverage
- Unit, integration, and edge case testing

### Clean Architecture
- Separation of concerns (Models → Interfaces → Services → Infrastructure → UI)
- Dependency Injection throughout
- No circular dependencies
- Easy to test and extend

### Design Patterns
- **Strategy Pattern**: Pluggable scoring algorithms
- **Dependency Injection**: Constructor-based for testability
- **Repository Pattern**: LessonManager for data access
- **Factory Pattern**: Service initialization

### Professional Practices
- Type hints throughout
- Comprehensive docstrings
- Validation with clear error messages
- Environment-based configuration
- Session state management

---

## ⚡ Quick Start

**Prerequisites:** Python 3.11+ and an OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

```bash
# Clone and setup
git clone https://github.com/emkoscielniak/broken_by_design.git
cd broken_by_design
python -m venv venv
source venv/bin/activate  # Mac/Linux (Windows: venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt

# Configure API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Run tests to verify
cd ai_learning_coach
pytest

# Launch the app
streamlit run app.py
```

✅ **Success!** The app opens at `http://localhost:8501`

### First Steps in the App:
1. **Prompt Analyzer**: Paste a prompt and click "Analyze"
2. **Lessons**: Start with "The Basics" (Level 1)
3. **History**: Review your analyzed prompts
4. **Settings**: Try different feedback styles in the sidebar

---

## 🎯 Example: Good vs Bad Prompts

### ❌ "Do It For Me" Prompt (Score: 35/100)
```
Write code for a calculator app
```
**Issues:**
- No learning intent
- Lacks context and specifics
- No engagement or verification
- Produces copy-paste dependency

### ✅ "Help Me Learn" Prompt (Score: 88/100)
```
I'm building a calculator app in Python. Can you explain how to structure 
the functions for add/subtract/multiply/divide operations? Then give me 
an example for the add() function, and let me try implementing subtract() 
myself. Review my implementation and suggest improvements.
```
**Strengths:**
- Clear learning goal
- Specific context (Python, calculator)
- Requests explanation before code
- Plans for practice and feedback
- Builds understanding, not just working code

**Broken by Design teaches you to write prompts like this through:**
- Real-time analysis and scoring
- Concrete suggestions for improvement
- Progressive lessons with exercises
- Tracking your growth over time

---

## � Technical Highlights

### Technologies Used
- **Python 3.11+**: Modern Python with type hints
- **Streamlit 1.50.0**: Rapid web UI development
- **OpenAI API**: gpt-4o-mini for chat and analysis
- **pytest**: Comprehensive testing framework
- **python-dotenv**: Environment configuration

### Architecture Patterns
```python
# Strategy Pattern Example
class IScoreStrategy(ABC):
    @abstractmethod
    def score(self, prompt: str) -> PromptScore:
        pass

class RubricScorer(IScoreStrategy):
    def score(self, prompt: str) -> PromptScore:
        # Scoring implementation
        pass

# Easy to add new strategies without changing existing code
```

### Test Coverage by Module
| Module | Tests | Coverage |
|--------|-------|----------|
| prompt_models.py | 22 | 100% |
| score_strategies.py | 14 | 96% |
| prompt_analyzer.py | 13 | 96% |
| feedback_generator.py | 12 | 94% |
| lesson_manager.py | 12 | 74% |
| **Overall** | **73** | **92.87%** |

---

## 🛠️ Development Commands

```bash
# Run all tests
cd ai_learning_coach
pytest

# Run tests with coverage report
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_models.py -v

# Run the Streamlit app
streamlit run app.py

# Run on different port (if 8501 is busy)
streamlit run app.py --server.port 8502
```

### Project Configuration
- **pytest.ini**: Test configuration and markers
- **.env**: OpenAI API key (create from .env.example)
- **.streamlit/config.toml**: Streamlit settings (disables telemetry)
- **requirements.txt**: Python dependencies

---

## 🚀 Extending the Project

**Want to add features? Here are some ideas:**

### Easy Extensions
- Add new lessons with exercises
- Create additional scoring criteria
- Implement new feedback styles
- Customize the UI theme and layout
- Add more anti-patterns to detect

### Moderate Extensions
- Database persistence for user progress
- User authentication system
- Export progress reports to PDF
- Analytics dashboard for admins
- Multi-language support

### Advanced Extensions
- Real-time collaboration features
- AI-generated personalized lessons
- Integration with other AI APIs (Claude, Gemini)
- Gamification with achievements and leaderboards
- A/B testing for different teaching approaches

**Each feature can be built using the same SOLID principles and TDD methodology demonstrated in the existing code.**

---

## � Documentation

**Core Documentation:**
- **[Streamlit Guide](ai_learning_coach/docs/STREAMLIT_GUIDE.md)** - Complete Streamlit tutorial
- **[Architecture Overview](docs/architecture.md)** - System design and patterns
- **[TDD Workflow](docs/TDD_WORKFLOW.md)** - Test-driven development process

**Development Guides:**
- **[Code as Textbook](docs/CODE_AS_TEXTBOOK.md)** - How the code teaches
- **[AI Collaboration](docs/AI_COLLABORATION.md)** - Working with AI tools
- **[Git Workflow](docs/GIT_WORKFLOW.md)** - Professional version control

**Course Materials:**
- **[Course Structure](docs/COURSE_STRUCTURE.md)** - 2-week learning plan
- **[Student Guide](docs/STUDENT_GUIDE.md)** - Day-by-day checklist
- **[Grading Rubric](docs/GRADING.md)** - Evaluation criteria

---

## 🤝 Contributing

This project demonstrates professional software development practices. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests first (TDD!)
4. Implement your feature
5. Ensure all tests pass (`pytest`)
6. Commit with clear messages (`git commit -m 'Add: amazing feature'`)
7. Push to your branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

**Please maintain:**
- 90%+ test coverage
- SOLID principles
- Type hints and docstrings
- Clean architecture patterns

---

## 📄 License

This project is part of an educational initiative. See the repository for license details.

---

<div align="center">

**✸ Broken by Design ✸**

*Teaching better AI prompting through deliberate practice*

**[Try It Now](#-quick-start)** • **[View Code](ai_learning_coach/src/)** • **[Read Docs](docs/)**

Built with ❤️ using SOLID principles and Test-Driven Development

</div>
