"""
Broken by Design - Ragebait Chatbot Interface

An AI chatbot that deliberately does the OPPOSITE of what you want.
Watch your emotional state deteriorate in real-time!

"Getting Over It with Bennett Foddy" meets ChatGPT.
"""

import streamlit as st
from datetime import datetime
from typing import Optional

# Import ragebait services
from src.services.rage_session_manager import RageSessionManager
from src.models.ragebait_models import EmotionalState, RageQuitResult

# Page configuration - Dark theme for maximum frustration ambiance
st.set_page_config(
    page_title="Broken by Design - Ragebait Chat",
    page_icon="😈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for ragebait aesthetic
st.markdown("""
<style>
    /* Dark theme with ominous red accents */
    .main {
        background-color: #1a1a1a;
        color: #e0e0e0;
    }
    
    /* Frustration meter styling */
    .frustration-meter {
        background: linear-gradient(90deg, #2ecc71, #f39c12, #e74c3c);
        height: 30px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Attempt counter - prominently displayed */
    .attempt-counter {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        color: #e74c3c;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin: 20px 0;
    }
    
    /* Emotional state display */
    .emotional-state {
        font-size: 2em;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .state-optimistic { background-color: #2ecc71; color: white; }
    .state-confused { background-color: #3498db; color: white; }
    .state-frustrated { background-color: #f39c12; color: white; }
    .state-angry { background-color: #e67e22; color: white; }
    .state-enraged { background-color: #e74c3c; color: white; }
    .state-broken { background-color: #95a5a6; color: white; }
    .state-transcendent { background-color: #9b59b6; color: white; }
    
    /* Chat message styling - DELIBERATELY ANNOYING */
    .user-message {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #3498db;
        color: #3a3a3a;  /* Barely readable - intentionally frustrating */
        font-size: 0.9em;
    }
    
    .ai-message {
        background-color: #2c3e50;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 4px solid #e74c3c;
        color: #ffffff;  /* AI message is bright and clear - mocking you */
        font-size: 1.1em;
        font-weight: bold;
    }
    
    /* Chat history container - deliberately cramped */
    .chat-history {
        max-height: 200px;  /* Tiny scroll area - annoying! */
        overflow-y: auto;
        padding: 10px;
        background-color: #0a0a0a;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    /* Philosophical commentary - Bennett Foddy style */
    .philosophical {
        font-size: 1.5em;
        font-style: italic;
        text-align: center;
        padding: 40px;
        margin: 40px 0;
        background-color: #2c3e50;
        border-radius: 15px;
        line-height: 1.8;
        color: #ecf0f1;
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
    }
    
    /* Give Up button - tempting red */
    .stButton > button {
        background-color: #c0392b;
        color: white;
        font-size: 1.2em;
        padding: 15px 30px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #e74c3c;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_services():
    """Initialize ragebait services (cached)."""
    manager = RageSessionManager()
    return manager


def initialize_session_state():
    """Initialize session state for ragebait chat."""
    if 'session_started' not in st.session_state:
        st.session_state.session_started = False
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'show_rage_quit' not in st.session_state:
        st.session_state.show_rage_quit = False
    
    if 'rage_quit_result' not in st.session_state:
        st.session_state.rage_quit_result = None


def render_frustration_meter(emotional_state: EmotionalState, attempt_count: int):
    """Render visual frustration meter showing emotional progression."""
    
    # Emoji mapping for each state
    state_emojis = {
        EmotionalState.OPTIMISTIC: "😊",
        EmotionalState.CONFUSED: "🤔",
        EmotionalState.FRUSTRATED: "😤",
        EmotionalState.ANGRY: "😠",
        EmotionalState.ENRAGED: "🤬",
        EmotionalState.BROKEN: "💀",
        EmotionalState.TRANSCENDENT: "🧘"
    }
    
    # Progress calculation (0-100%)
    state_progress = {
        EmotionalState.OPTIMISTIC: 0,
        EmotionalState.CONFUSED: 16,
        EmotionalState.FRUSTRATED: 33,
        EmotionalState.ANGRY: 50,
        EmotionalState.ENRAGED: 66,
        EmotionalState.BROKEN: 83,
        EmotionalState.TRANSCENDENT: 100
    }
    
    progress = state_progress.get(emotional_state, 0)
    emoji = state_emojis.get(emotional_state, "😊")
    
    # Display attempt counter
    st.markdown(
        f'<div class="attempt-counter">Attempt #{attempt_count}</div>',
        unsafe_allow_html=True
    )
    
    # Display emotional state with styling
    state_class = f"state-{emotional_state.value}"
    st.markdown(
        f'<div class="emotional-state {state_class}">'
        f'{emoji} {emotional_state.value.upper()} {emoji}'
        f'</div>',
        unsafe_allow_html=True
    )
    
    # Progress bar
    st.progress(progress / 100.0)
    
    # State description
    descriptions = {
        EmotionalState.OPTIMISTIC: "Fresh and hopeful! This AI will surely help me...",
        EmotionalState.CONFUSED: "Wait, that's not what I asked for...",
        EmotionalState.FRUSTRATED: "Why won't it just answer my question?!",
        EmotionalState.ANGRY: "This is ridiculous! Just do what I ask!",
        EmotionalState.ENRAGED: "CAPS LOCK ENGAGED. RAGE MODE ACTIVATED.",
        EmotionalState.BROKEN: "I give up. This is pointless. Everything is pointless.",
        EmotionalState.TRANSCENDENT: "Beyond anger. Beyond hope. One with the void."
    }
    
    st.info(descriptions.get(emotional_state, ""))


def render_chat_history(chat_history: list):
    """Render chat history with user and AI messages."""
    st.markdown("---")
    st.subheader("💬 Conversation History")
    
    for message in chat_history:
        # User message
        st.markdown(
            f'<div class="user-message">'
            f'<strong>You:</strong> {message["prompt"]}'
            f'</div>',
            unsafe_allow_html=True
        )
        
        # AI response
        st.markdown(
            f'<div class="ai-message">'
            f'<strong>AI:</strong> {message["response"]}'
            f'</div>',
            unsafe_allow_html=True
        )


def render_rage_quit_result(result: RageQuitResult):
    """Display the final rage quit result with Bennett Foddy style commentary."""
    
    st.markdown("---")
    st.markdown("## 🏳️ You Gave Up")
    
    # Philosophical commentary - large and contemplative
    st.markdown(
        f'<div class="philosophical">{result.philosophical_commentary}</div>',
        unsafe_allow_html=True
    )
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Attempts",
            result.frustration_score.total_attempts,
            help="How many times you tried before giving up"
        )
        st.metric(
            "Max Rage Level",
            result.frustration_score.max_rage_level,
            help="Highest emotional intensity reached"
        )
    
    with col2:
        st.metric(
            "Time Invested",
            f"{result.frustration_score.time_elapsed_seconds}s",
            help="How long you persisted in your futile struggle"
        )
        st.metric(
            "Politeness Decay",
            f"{result.frustration_score.politeness_decay:.1f}%",
            help="How much your courtesy deteriorated"
        )
    
    with col3:
        st.metric(
            "Entertaining Metric",
            f"{result.entertaining_metric:.1f}",
            help="How entertaining was your suffering? (0-100)"
        )
        st.metric(
            "Persistence Rating",
            result.frustration_score.persistence_rating,
            help="Your stubbornness classification"
        )
    
    # Legendary status?
    if result.frustration_score.is_legendary:
        st.balloons()
        st.success("🏆 LEGENDARY STATUS ACHIEVED! Your suffering was truly remarkable.")
    
    # Achievement
    if result.achievement_unlocked:
        st.info(f"🎖️ Achievement Unlocked: {result.achievement_unlocked}")
    
    # Additional metrics
    st.markdown("---")
    st.subheader("📊 Detailed Metrics")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Profanity Creativity:** {result.frustration_score.profanity_creativity}")
    with col2:
        st.write(f"**Caps Lock Escalation:** {result.frustration_score.caps_lock_escalation}")
    with col3:
        st.write(f"**Philosophical Score:** {result.frustration_score.philosophical_score:.1f}")


def main():
    """Main application entry point."""
    
    # Initialize
    manager = initialize_services()
    initialize_session_state()
    
    # Title with ominous subtitle
    st.title("😈 Broken by Design")
    st.markdown(
        "*An AI chatbot that deliberately does the **OPPOSITE** of what you want.*"
    )
    
    # Start session button
    if not st.session_state.session_started:
        st.markdown("---")
        st.markdown("### Ready to experience frustration?")
        st.write("This AI will:")
        st.write("- Deliberately misunderstand your questions")
        st.write("- Provide confidently incorrect answers")
        st.write("- Redirect conversations to irrelevant topics")
        st.write("- Track your emotional deterioration in real-time")
        st.write("- Calculate how entertaining your suffering is")
        
        if st.button("🎯 Start Chat Session", use_container_width=True):
            manager.start_session(user_id="streamlit_user")
            st.session_state.session_started = True
            st.rerun()
        
        return
    
    # Get current session
    session = manager.session
    if session is None:
        st.error("Session error. Please refresh the page.")
        return
    
    # Show rage quit result if user gave up
    if st.session_state.show_rage_quit and st.session_state.rage_quit_result:
        render_rage_quit_result(st.session_state.rage_quit_result)
        
        # Option to start over
        if st.button("🔄 Try Again (You Glutton for Punishment)", use_container_width=True):
            st.session_state.session_started = False
            st.session_state.chat_history = []
            st.session_state.show_rage_quit = False
            st.session_state.rage_quit_result = None
            st.rerun()
        
        return
    
    # Display frustration meter
    render_frustration_meter(session.current_emotional_state, len(session.attempts))
    
    # Chat interface
    st.markdown("---")
    
    # User input FIRST - So you can't see your history while typing (annoying!)
    user_prompt = st.text_input(
        "💭 What do you want the AI to help you with?",
        placeholder="Try asking for help with Python, JavaScript, Git, etc...",
        key="user_input"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        submit_button = st.button("📤 Send Message", use_container_width=True)
    
    with col2:
        # Show Give Up button if conditions are met
        if manager.should_offer_rage_quit():
            give_up_button = st.button("🏳️ Give Up", use_container_width=True, type="primary")
            if give_up_button:
                # Generate rage quit result
                result = manager.generate_rage_quit_result()
                st.session_state.rage_quit_result = result
                st.session_state.show_rage_quit = True
                st.rerun()
    
    # Process user message
    if submit_button and user_prompt:
        # Process through manager
        response, emotional_state, attempt = manager.process_prompt(user_prompt)
        
        # Add to chat history
        st.session_state.chat_history.append({
            "prompt": user_prompt,
            "response": response,
            "emotional_state": emotional_state.value,
            "attempt_number": attempt.attempt_number
        })
        
        # Clear input and rerun
        st.rerun()
    
    # Display chat history BELOW (after you've already typed - frustrating!)
    if st.session_state.chat_history:
        render_chat_history(st.session_state.chat_history)
    else:
        st.info("👆 Type a message above to start your descent into frustration...")
    
    # Session statistics in sidebar
    with st.sidebar:
        st.markdown("### 📊 Session Stats")
        summary = manager.get_session_summary()
        
        if summary.get("active"):
            st.write(f"**Attempts:** {summary['attempt_count']}")
            st.write(f"**Duration:** {summary['duration_display']}")
            st.write(f"**Current State:** {summary['current_emotional_state']}")
            st.write(f"**Politeness Decay:** {summary['politeness_decay']:.1f}%")
            st.write(f"**Profanity Count:** {summary['profanity_count']}")
            st.write(f"**Max Caps %:** {summary['max_caps_percentage']:.1f}%")
            
            if summary['rage_quit_available']:
                st.warning("🏳️ You can give up now...")
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.write("This chatbot is designed to frustrate you.")
        st.write("It uses SOLID principles and TDD methodology.")
        st.write("The irony: deliberately terrible UX with excellent code quality.")


if __name__ == "__main__":
    main()
