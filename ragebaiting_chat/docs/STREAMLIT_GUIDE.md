# Streamlit Guide for AI Learning Coach

## What is Streamlit?

Streamlit is a Python framework for building interactive web applications quickly. It's perfect for data science and ML applications because you can create UIs with pure Python - no HTML, CSS, or JavaScript required.

## Key Concepts

### 1. Script Re-runs
Every time a user interacts with a widget, Streamlit re-runs the entire script from top to bottom. This makes it easy to reason about but requires thoughtful state management.

### 2. Session State
Use `st.session_state` to persist data across re-runs:
```python
# Initialize
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# Use
st.session_state.counter += 1
```

### 3. Widgets
Common interactive elements:
- `st.button()` - Click buttons
- `st.text_input()` - Text fields
- `st.text_area()` - Multi-line text
- `st.selectbox()` - Dropdown menus
- `st.radio()` - Radio buttons
- `st.checkbox()` - Checkboxes
- `st.slider()` - Sliders

### 4. Display Elements
Ways to show content:
- `st.write()` - Universal display function
- `st.markdown()` - Markdown formatting
- `st.code()` - Code blocks with syntax highlighting
- `st.success()` / `st.error()` / `st.warning()` / `st.info()` - Colored messages
- `st.expander()` - Collapsible sections

## Running Your Streamlit App

### Development Mode
```bash
streamlit run app.py
```

### Production Mode
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Environment Variables
Create a `.streamlit/secrets.toml` file:
```toml
OPENAI_API_KEY = "your-api-key-here"
```

Or use `.env` with python-dotenv (which we're using).

## Best Practices for This Project

### 1. Initialize Services Once
Use `@st.cache_resource` to create services only once:
```python
@st.cache_resource
def get_services():
    scorer = RubricScorer()
    analyzer = PromptAnalyzer(scorer)
    generator = FeedbackGenerator()
    return scorer, analyzer, generator
```

### 2. Manage User Progress
Store progress in session state:
```python
if 'progress' not in st.session_state:
    st.session_state.progress = UserProgress(
        user_id="streamlit_user",
        current_lesson=1,
        completed_lessons=[],
        prompt_history=[],
        skill_level=1,
        total_prompts=0,
        good_prompts=0
    )
```

### 3. Layout Options
- **Sidebar**: `st.sidebar.title("Navigation")`
- **Columns**: `col1, col2 = st.columns(2)`
- **Tabs**: `tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])`
- **Expanders**: `with st.expander("Details"):`

### 4. Styling
Use markdown and custom CSS:
```python
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    """, unsafe_allow_html=True)
```

## Streamlit Commands

- `streamlit run app.py` - Start the app
- `streamlit hello` - Run demo app
- `streamlit docs` - Open documentation
- `streamlit cache clear` - Clear cache
- `streamlit config show` - Show configuration

## Debugging Tips

1. **Print statements work**: Use `st.write()` to debug
2. **Check session state**: `st.write(st.session_state)`
3. **Use expanders**: Hide debug info in expanders
4. **Rerun button**: Add `st.experimental_rerun()` for manual reruns

## Deployment

### Streamlit Community Cloud (Free)
1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect your repo
4. Add secrets in dashboard
5. Deploy!

### Other Options
- Docker container
- Heroku
- AWS/GCP/Azure
- Your own server

## Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Cheat Sheet](https://docs.streamlit.io/library/cheatsheet)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [Streamlit Forum](https://discuss.streamlit.io)

## Common Patterns for AI Learning Coach

### Pattern 1: Prompt Analysis Flow
```python
# User inputs prompt
user_prompt = st.text_area("Enter your prompt:")

# Analyze on button click
if st.button("Analyze"):
    analysis = analyzer.evaluate(user_prompt)
    
    # Display results
    st.metric("Score", f"{analysis.score.total_score:.0f}/100")
    
    if analysis.strengths:
        st.success("Strengths")
        for strength in analysis.strengths:
            st.write(f"✓ {strength}")
    
    if analysis.improvements:
        st.warning("Improvements")
        for improvement in analysis.improvements:
            st.write(f"💡 {improvement}")
```

### Pattern 2: Progress Tracking
```python
# Display progress
col1, col2, col3 = st.columns(3)
col1.metric("Total Prompts", st.session_state.progress.total_prompts)
col2.metric("Success Rate", f"{st.session_state.progress.success_rate:.1f}%")
col3.metric("Skill Level", st.session_state.progress.skill_level)
```

### Pattern 3: Lesson Navigation
```python
# Sidebar navigation
with st.sidebar:
    st.title("📚 Lessons")
    lesson = st.selectbox(
        "Choose a lesson",
        options=available_lessons,
        format_func=lambda x: x.title
    )
    
    if st.button("Start Lesson"):
        st.session_state.current_lesson = lesson
```

## Tips for This Project

1. **Keep state minimal**: Only store what you need between reruns
2. **Use callbacks**: For complex interactions, use widget callbacks
3. **Cache expensive operations**: Use `@st.cache_data` for data processing
4. **Clear cache when needed**: Use `st.cache_resource.clear()` or `st.cache_data.clear()`
5. **Test locally first**: Always test with `streamlit run` before deploying
6. **Handle errors gracefully**: Use try/except and display friendly messages
7. **Show loading states**: Use `st.spinner()` for long operations

## Example: API Key Handling

```python
import os
from dotenv import load_dotenv

# Load from .env
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OpenAI API key not found!")
    st.info("Please add OPENAI_API_KEY to your .env file")
    st.stop()  # Stop execution

# Use the key
client = OpenAI(api_key=api_key)
```
