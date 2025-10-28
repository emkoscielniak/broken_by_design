"""
Broken by Design - Streamlit Web Application

A web interface for learning how to prompt AI effectively.
Demonstrates SOLID principles and clean architecture in action.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Import our services
from src.services import (
    RubricScorer,
    PromptAnalyzer,
    FeedbackGenerator,
    LessonManager,
    PromptDemonstrator,
)
from src.models import UserProgress, PromptAnalysis
from src.infrastructure import OpenAIClient

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Broken By Design",
    page_icon="✸",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def initialize_services():
    """Initialize all services (cached to avoid recreation on reruns)."""
    scorer = RubricScorer()
    analyzer = PromptAnalyzer(scorer)
    feedback_generator = FeedbackGenerator(style="encouraging")
    lesson_manager = LessonManager()
    lesson_manager.load_default_lessons()
    
    # Initialize OpenAI client if API key available
    api_key = os.getenv("OPENAI_API_KEY")
    ai_client = OpenAIClient(api_key) if api_key else None
    
    # Initialize demonstrator with AI client
    demonstrator = PromptDemonstrator(ai_client)
    
    return scorer, analyzer, feedback_generator, lesson_manager, ai_client, demonstrator


def initialize_session_state():
    """Initialize session state variables."""
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
    
    if 'feedback_style' not in st.session_state:
        st.session_state.feedback_style = "encouraging"
    
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None
    
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None


def render_sidebar(lesson_manager):
    """Render sidebar with navigation and progress."""
    with st.sidebar:
        st.title("🎓 Broken by Design")
        st.markdown("---")
        
        # Optional email for saving progress
        st.subheader("💾 Save Your Progress")
        if st.session_state.user_email:
            st.success(f"✅ Saving to: {st.session_state.user_email}")
            if st.button("🔓 Change Email", use_container_width=True):
                st.session_state.user_email = None
                st.rerun()
        else:
            email_input = st.text_input(
                "Email (optional)",
                placeholder="your.email@example.com",
                help="Enter your email to save your lessons and progress data"
            )
            if st.button("💾 Save My Progress", use_container_width=True):
                if email_input and "@" in email_input:
                    st.session_state.user_email = email_input
                    st.session_state.progress.user_id = email_input
                    st.success("✅ Progress will be saved!")
                    st.rerun()
                elif email_input:
                    st.error("Please enter a valid email address")
        
        st.markdown("---")
        
        # Progress metrics
        st.subheader("📊 Your Progress")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Prompts", st.session_state.progress.total_prompts)
            st.metric("Skill Level", st.session_state.progress.skill_level)
        with col2:
            st.metric("Good Prompts", st.session_state.progress.good_prompts)
            success_rate = st.session_state.progress.success_rate
            st.metric("Success Rate", f"{success_rate:.1f}%")
        
        st.markdown("---")
        
        # Feedback style selector
        st.subheader("💬 Feedback Style")
        feedback_style = st.selectbox(
            "Choose your feedback style:",
            options=["encouraging", "direct", "socratic"],
            index=["encouraging", "direct", "socratic"].index(st.session_state.feedback_style),
            help="Encouraging: Positive and supportive\nDirect: Straightforward facts\nSocratic: Question-based reflection"
        )
        if feedback_style != st.session_state.feedback_style:
            st.session_state.feedback_style = feedback_style
            st.rerun()
        
        st.markdown("---")
        
        # Available lessons
        st.subheader("📚 Available Lessons")
        all_lessons = lesson_manager.get_all_lessons()
        for lesson in sorted(all_lessons, key=lambda x: x.difficulty):
            completed = "✅" if lesson.id in st.session_state.progress.completed_lessons else "📖"
            st.markdown(f"{completed} **{lesson.title}**")
            st.caption(f"Level {lesson.difficulty} - {lesson.description}")
            st.markdown("")


def render_prompt_analyzer(analyzer, feedback_generator):
    """Render the main prompt analysis interface."""
    st.header("✍️ Prompt Analysis")
    st.markdown("Enter a prompt below and get instant feedback on how to improve it for better learning.")
    
    # Prompt input
    user_prompt = st.text_area(
        "Your Prompt:",
        height=150,
        placeholder="Example: Explain Python decorators with examples, then quiz me to check my understanding",
        help="Try to be specific and learning-oriented!"
    )
    
    # Analyze button
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        analyze_button = st.button("🔍 Analyze Prompt", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.current_analysis = None
            st.rerun()
    
    if analyze_button and user_prompt.strip():
        with st.spinner("Analyzing your prompt..."):
            # Analyze the prompt
            analysis = analyzer.evaluate(user_prompt)
            
            # Update progress
            st.session_state.progress.total_prompts += 1
            if analysis.score.is_passing:
                st.session_state.progress.good_prompts += 1
            
            # Add to history
            st.session_state.progress.prompt_history.append(analysis)
            
            # Store current analysis
            st.session_state.current_analysis = analysis
            st.rerun()
    
    # Display analysis results
    if st.session_state.current_analysis:
        analysis = st.session_state.current_analysis
        
        st.markdown("---")
        st.subheader("📈 Analysis Results")
        
        # Score metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            score_color = "🟢" if analysis.score.is_passing else "🔴"
            st.metric(
                "Overall Score",
                f"{score_color} {analysis.score.total_score:.0f}/100",
                delta="Passing" if analysis.score.is_passing else "Needs Work"
            )
        with col2:
            st.metric("Learning", f"{analysis.score.learning_orientation:.0f}/100")
        with col3:
            st.metric("Specificity", f"{analysis.score.specificity:.0f}/100")
        with col4:
            st.metric("Engagement", f"{analysis.score.engagement:.0f}/100")
        
        # Intent badge
        intent_emoji = {
            "do_it_for_me": "🚫",
            "help_me_learn": "✅",
            "clarifying": "❓",
            "reflection": "🤔",
            "unknown": "❔"
        }
        st.markdown(f"**Intent:** {intent_emoji.get(analysis.score.intent.value, '❔')} {analysis.score.intent.value.replace('_', ' ').title()}")
        
        st.markdown("---")
        
        # Generate and display feedback
        feedback_generator.style = st.session_state.feedback_style
        feedback = feedback_generator.generate_feedback(analysis)
        
        st.subheader("💬 Personalized Feedback")
        st.markdown(feedback)


def render_lessons(lesson_manager):
    """Render lessons interface."""
    st.header("📚 Lessons")
    
    # Get recommended lesson
    next_lesson = lesson_manager.get_next_lesson(st.session_state.progress)
    
    if next_lesson:
        st.info(f"🎯 **Recommended:** {next_lesson.title} (Level {next_lesson.difficulty})")
    
    # Display all lessons
    st.markdown("### All Lessons")
    
    all_lessons = lesson_manager.get_all_lessons()
    for lesson in sorted(all_lessons, key=lambda x: x.difficulty):
        is_completed = lesson.id in st.session_state.progress.completed_lessons
        
        with st.expander(f"{'✅' if is_completed else '📖'} {lesson.title} - Level {lesson.difficulty}"):
            st.markdown(f"**Description:** {lesson.description}")
            
            st.markdown("**Learning Objectives:**")
            for obj in lesson.learning_objectives:
                st.markdown(f"- {obj}")
            
            st.markdown(f"**Content:**\n{lesson.content}")
            
            if lesson.exercises:
                st.markdown("**Exercises:**")
                for i, exercise in enumerate(lesson.exercises, 1):
                    st.markdown(f"{i}. {exercise.prompt}")
                    with st.expander("View hints and examples"):
                        st.markdown("**Hints:**")
                        for hint in exercise.hints:
                            st.markdown(f"💡 {hint}")
                        st.markdown(f"**Good Example:** {exercise.good_example}")
                        st.markdown(f"**Bad Example:** ❌ {exercise.bad_example}")
            
            if not is_completed:
                if st.button(f"Mark '{lesson.title}' as Complete", key=f"complete_{lesson.id}"):
                    st.session_state.progress.completed_lessons.append(lesson.id)
                    # Update skill level based on completed lessons
                    completed_count = len(st.session_state.progress.completed_lessons)
                    new_skill = min(5, 1 + (completed_count // 2))
                    st.session_state.progress.skill_level = new_skill
                    st.success(f"🎉 Completed {lesson.title}!")
                    st.rerun()


def render_history():
    """Render prompt history."""
    st.header("📜 Prompt History")
    
    if not st.session_state.progress.prompt_history:
        st.info("No prompts analyzed yet. Go to the Prompt Analyzer to get started!")
        return
    
    st.markdown(f"**Total prompts analyzed:** {len(st.session_state.progress.prompt_history)}")
    
    # Show recent prompts (last 10)
    recent_prompts = list(reversed(st.session_state.progress.prompt_history[-10:]))
    
    for i, analysis in enumerate(recent_prompts, 1):
        score_emoji = "✅" if analysis.score.is_passing else "❌"
        with st.expander(f"{score_emoji} {analysis.prompt[:50]}... ({analysis.score.total_score:.0f}/100)"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Learning", f"{analysis.score.learning_orientation:.0f}")
            with col2:
                st.metric("Specificity", f"{analysis.score.specificity:.0f}")
            with col3:
                st.metric("Engagement", f"{analysis.score.engagement:.0f}")
            
            if analysis.strengths:
                st.markdown("**Strengths:**")
                for strength in analysis.strengths:
                    st.markdown(f"✓ {strength}")
            
            if analysis.detected_patterns:
                st.markdown("**Issues:**")
                for pattern in analysis.detected_patterns:
                    st.markdown(f"⚠️ {pattern}")


def render_demonstration(demonstrator, ai_client):
    """Render the 'See It In Action' demonstration interface."""
    st.header("🎭 See It In Action")
    st.markdown("""
    **Experience the difference between bad and good prompts in real-time.**
    
    Enter a prompt below and see how AI responds differently when the prompt is poorly vs well-crafted.
    This demonstrates why prompt quality matters for learning.
    """)
    
    # Check if API is available
    if not ai_client:
        st.info("💡 **Demo Mode**: Using simulated responses (OpenAI API key not configured)")
    else:
        st.success("✅ **Live Mode**: Using real OpenAI API responses")
    
    # Prompt input
    user_prompt = st.text_area(
        "Enter your prompt:",
        height=100,
        placeholder="Example: Write code for a calculator",
        help="Try a typical prompt you might use with AI"
    )
    
    # Optional: User can provide their own improved version
    col1, col2 = st.columns([3, 1])
    with col1:
        custom_improved = st.text_area(
            "Or provide your improved version (optional):",
            height=100,
            placeholder="Leave blank to auto-generate an improved version",
            help="If you have an improved version in mind, enter it here"
        )
    with col2:
        st.markdown("") # Spacing
        st.markdown("") # Spacing
        demonstrate_button = st.button(
            "🎭 Show the Difference",
            type="primary",
            use_container_width=True
        )
    
    if demonstrate_button and user_prompt.strip():
        with st.spinner("Generating responses... This may take a few seconds"):
            # Get demonstration
            improved_prompt = custom_improved.strip() if custom_improved.strip() else None
            result = demonstrator.demonstrate(user_prompt, improved_prompt)
            
            # Store in session state
            st.session_state.current_demonstration = result
            st.rerun()
    
    # Display results
    if 'current_demonstration' in st.session_state and st.session_state.current_demonstration:
        result = st.session_state.current_demonstration
        
        st.markdown("---")
        st.subheader("📊 The Difference")
        
        if result.is_simulated:
            st.info("🎭 **Simulated Demo**: These are example responses showing typical patterns")
        else:
            st.success("✅ **Live Results**: Real responses from OpenAI API")
        
        # Side-by-side comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ❌ Original Prompt")
            st.code(result.original_prompt, language=None)
            st.markdown("**AI Response:**")
            with st.container():
                st.markdown(
                    f'<div style="background-color: #ffe6e6; padding: 15px; border-radius: 5px; border-left: 4px solid #ff4444;">{result.bad_response}</div>',
                    unsafe_allow_html=True
                )
            st.caption("⚠️ Unhelpful: Just gives answers without teaching")
        
        with col2:
            st.markdown("### ✅ Improved Prompt")
            st.code(result.improved_prompt, language=None)
            st.markdown("**AI Response:**")
            with st.container():
                st.markdown(
                    f'<div style="background-color: #e6f7e6; padding: 15px; border-radius: 5px; border-left: 4px solid #44ff44;">{result.good_response}</div>',
                    unsafe_allow_html=True
                )
            st.caption("✅ Helpful: Explains, demonstrates, and encourages practice")
        
        # Explanation
        st.markdown("---")
        st.subheader("💡 Why This Matters")
        st.markdown(result.explanation)
        
        # Clear button
        if st.button("🗑️ Clear Demo", use_container_width=False):
            st.session_state.current_demonstration = None
            st.rerun()


def main():
    """Main application entry point."""
    # Initialize
    initialize_session_state()
    scorer, analyzer, feedback_generator, lesson_manager, ai_client, demonstrator = initialize_services()
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        st.warning("⚠️ OpenAI API key not found. Demo mode will use simulated responses. Add OPENAI_API_KEY to your .env file for live demonstrations.")
    
    # Render sidebar
    render_sidebar(lesson_manager)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "✍️ Prompt Analyzer",
        "🎭 See It In Action",
        "📚 Lessons",
        "📜 History"
    ])
    
    with tab1:
        render_prompt_analyzer(analyzer, feedback_generator)
    
    with tab2:
        render_demonstration(demonstrator, ai_client)
    
    with tab3:
        render_lessons(lesson_manager)
    
    with tab4:
        render_history()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<center>Built with ❤️ using SOLID principles and Test-Driven Development | "
        "<a href='https://github.com'>View Source</a></center>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
# touch test
