# Running the AI Learning Coach Web App

## Quick Start

1. **Ensure you have the OpenAI API key in your `.env` file:**
   ```bash
   cd /Users/emisk/is218/broken_by_design/ai_learning_coach
   ```

2. **Make sure the `.env` file exists with your API key:**
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** to the URL shown (usually http://localhost:8501)

## Features

### 🎓 Prompt Analyzer
- Enter any prompt and get instant feedback
- See your score breakdown (learning orientation, specificity, engagement)
- Get personalized improvement suggestions
- View example better prompts

### 📚 Lessons
- 5 structured lessons from beginner to advanced
- Learning objectives and content
- Practice exercises with hints
- Track completed lessons

### 📜 History
- View all your analyzed prompts
- See your improvement over time
- Review past feedback

### 💬 Feedback Styles
Choose your preferred feedback style:
- **Encouraging**: Positive and motivational
- **Direct**: Straightforward facts and metrics
- **Socratic**: Question-based, reflective guidance

## How It Works

The app uses the same core services as the terminal version:

1. **RubricScorer**: Evaluates prompts using rule-based scoring
2. **PromptAnalyzer**: Detects anti-patterns and identifies strengths
3. **FeedbackGenerator**: Creates personalized feedback in different styles
4. **LessonManager**: Recommends lessons based on your progress

## Navigation

- **Sidebar**: View your progress, change feedback style, see available lessons
- **Prompt Analyzer Tab**: Main interface for analyzing prompts
- **Lessons Tab**: Browse and complete lessons
- **History Tab**: Review your past prompts

## Tips

1. **Start with Lesson 1**: Learn the basics of good prompting
2. **Try different feedback styles**: See which one helps you learn best
3. **Practice regularly**: The more prompts you analyze, the better you'll get
4. **Complete lessons**: Unlock higher difficulty levels
5. **Review history**: See how your prompts improve over time

## Keyboard Shortcuts

- `Ctrl/Cmd + Enter` in text area: Submit prompt
- `R`: Rerun the app
- `C`: Clear cache

## Troubleshooting

### App won't start
```bash
# Check if streamlit is installed
pip list | grep streamlit

# Reinstall if needed
pip install streamlit
```

### API key not working
```bash
# Check your .env file
cat .env

# Make sure it's in the right directory
pwd
```

### Port already in use
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

### Clear cache if things look weird
```bash
# In the app, click the hamburger menu (☰) → Settings → Clear Cache
# Or press 'C' key
```

## Development

### Watch for file changes (auto-reload)
Streamlit automatically watches for file changes and reloads!

### Debug mode
```bash
streamlit run app.py --logger.level=debug
```

### Custom config
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"

[server]
port = 8501
```

## Deployment

See [STREAMLIT_GUIDE.md](docs/STREAMLIT_GUIDE.md) for deployment options.

## Architecture

The Streamlit app maintains the same clean architecture:
- **Models**: Data structures (unchanged)
- **Interfaces**: Service contracts (unchanged)
- **Services**: Business logic (unchanged)
- **Infrastructure**: OpenAI client, persistence
- **UI**: Streamlit interface (new!)

This demonstrates the power of SOLID principles - we added a completely new UI without changing any core business logic!
