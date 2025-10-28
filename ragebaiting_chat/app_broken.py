"""
Broken by Design - ANTI-SOLID Version

This version deliberately violates SOLID principles while remaining functional.
Uses a God Object that does everything in one massive class.

Educational value: Shows WHY we use SOLID principles by breaking them all.
"""

import streamlit as st
from src.services.god_object import GodObject

# Page configuration
st.set_page_config(
    page_title="Broken by Design",
    page_icon="💩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Violation: Inline CSS instead of separate styling module
st.markdown("""
<style>
    .main { background-color: #1a1a1a; color: #e0e0e0; }
    .attempt-counter { font-size: 3em; font-weight: bold; text-align: center; color: #e74c3c; }
    .emotional-state { font-size: 2em; text-align: center; padding: 20px; border-radius: 10px; margin: 20px 0; }
    .user-message { background-color: #1a1a1a; padding: 15px; border-radius: 10px; margin: 10px 0; color: #3a3a3a; font-size: 0.9em; }
    .ai-message { background-color: #2c3e50; padding: 15px; border-radius: 10px; margin: 10px 0; color: #ffffff; font-size: 1.1em; font-weight: bold; }
    .philosophical { font-size: 1.5em; font-style: italic; text-align: center; padding: 40px; background-color: #2c3e50; }
</style>
""", unsafe_allow_html=True)


# Violation: Global function instead of method in a class
def get_emoji_for_state(state: str) -> str:
    """Hardcoded emoji mapping."""
    emojis = {
        "optimistic": "😊",
        "confused": "🤔", 
        "frustrated": "😤",
        "angry": "😠",
        "enraged": "🤬",
        "broken": "💀",
        "transcendent": "🧘"
    }
    return emojis.get(state, "😊")


# Violation: Global function with hardcoded logic
def get_state_description(state: str) -> str:
    """Hardcoded state descriptions."""
    descriptions = {
        "optimistic": "Fresh and hopeful! This AI will surely help me...",
        "confused": "Wait, that's not what I asked for...",
        "frustrated": "Why won't it just answer my question?!",
        "angry": "This is ridiculous! Just do what I ask!",
        "enraged": "CAPS LOCK ENGAGED. RAGE MODE ACTIVATED.",
        "broken": "I give up. This is pointless. Everything is pointless.",
        "transcendent": "Beyond anger. Beyond hope. One with the void."
    }
    return descriptions.get(state, "")


# Violation: Initialize god object globally instead of dependency injection
@st.cache_resource
def get_god_object():
    """Create the god object that does everything."""
    return GodObject()


# Violation: Initialize session state with procedural code
def init_session():
    """Hardcoded session initialization."""
    if 'started' not in st.session_state:
        st.session_state.started = False
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'show_result' not in st.session_state:
        st.session_state.show_result = False
    if 'final_result' not in st.session_state:
        st.session_state.final_result = None


# Violation: Massive main function that does everything
def main():
    """The main function - does everything in one place."""
    
    god = get_god_object()
    init_session()
    
    # Title
    st.title("💩 Broken by Design")
    st.markdown("*An AI chatbot that's actively working against you.*")
    st.caption("Nothing works the way it should. That's the point.")
    
    # Start screen
    if not st.session_state.started:
        st.markdown("---")
        st.markdown("### Ready to experience pure chaos?")
        st.write("This AI will:")
        st.write("- 🎯 Miss your point entirely")
        st.write("- 🤡 Answer questions you didn't ask")
        st.write("- 🎪 Redirect every topic to something useless")
        st.write("- 📊 Track how long you last before giving up")
        st.write("- 🧘 Judge your persistence (or lack thereof)")
        st.write("")
        st.write("**Fair warning:** Nothing about this experience will be helpful.")
        
        if st.button("🎯 Start Chat Session", use_container_width=True):
            god.start(user_id="anti_solid_user")
            st.session_state.started = True
            st.rerun()
        return
    
    # Show result screen
    if st.session_state.show_result and st.session_state.final_result:
        st.markdown("---")
        st.markdown("## 🏳️ You Gave Up")
        
        result = st.session_state.final_result
        
        # Commentary
        st.markdown(
            f'<div class="philosophical">{result["commentary"]}</div>',
            unsafe_allow_html=True
        )
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Attempts", result["attempts"])
            st.metric("Max Rage Level", result["max_rage"])
        with col2:
            st.metric("Time Invested", f"{result['time_seconds']}s")
            st.metric("Profanity Count", result["profanity"])
        with col3:
            st.metric("Entertaining Metric", f"{result['entertaining_metric']:.1f}")
            st.metric("Persistence Rating", result["persistence_rating"])
        
        if st.button("🔄 Try Again", use_container_width=True):
            st.session_state.started = False
            st.session_state.history = []
            st.session_state.show_result = False
            st.session_state.final_result = None
            st.rerun()
        return
    
    # Display frustration meter
    stats = god.get_stats()
    if stats.get("active"):
        emoji = get_emoji_for_state(god.current_state)
        st.markdown(
            f'<div class="attempt-counter">Attempt #{stats["attempts"]}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="emotional-state">{emoji} {god.current_state.upper()} {emoji}</div>',
            unsafe_allow_html=True
        )
        st.info(get_state_description(god.current_state))
        
        # Progress bar (hardcoded values)
        progress_map = {
            "optimistic": 0,
            "confused": 16,
            "frustrated": 33,
            "angry": 50,
            "enraged": 66,
            "broken": 83,
            "transcendent": 100
        }
        st.progress(progress_map.get(god.current_state, 0) / 100.0)
    
    st.markdown("---")
    
    # Input field FIRST (annoying)
    user_input = st.text_input(
        "💭 What do you want the AI to help you with?",
        placeholder="Try asking for help...",
        key="input"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        send = st.button("📤 Send Message", use_container_width=True)
    with col2:
        # Inline logic instead of separate method
        stats = god.get_stats()
        if stats.get("active") and stats["attempts"] >= 5:
            if st.button("🏳️ Give Up", use_container_width=True, type="primary"):
                # Call the god object
                result = god.do_everything("")  # Empty to get current result
                if result.get("result"):
                    st.session_state.final_result = result["result"]
                    st.session_state.show_result = True
                    st.rerun()
    
    # Process message
    if send and user_input:
        # Call the god object that does EVERYTHING
        result = god.do_everything(user_input)
        
        # Add to history (duplicated logic)
        st.session_state.history.append({
            "prompt": user_input,
            "response": result["response"],
            "state": result["emotional_state"]
        })
        
        # Check if should quit
        if result["should_quit"] and result.get("result"):
            st.session_state.final_result = result["result"]
            st.session_state.show_result = True
        
        st.rerun()
    
    # Display history BELOW (annoying)
    if st.session_state.history:
        st.markdown("---")
        st.subheader("💬 Conversation History")
        
        # Inline rendering instead of separate function
        for msg in st.session_state.history:
            st.markdown(
                f'<div class="user-message"><strong>You:</strong> {msg["prompt"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="ai-message"><strong>AI:</strong> {msg["response"]}</div>',
                unsafe_allow_html=True
            )
    else:
        st.info("👆 Type a message above to start your descent into frustration...")
    
    # Sidebar (procedural style)
    with st.sidebar:
        st.markdown("### 📊 Session Stats")
        stats = god.get_stats()
        if stats.get("active"):
            # Inline display instead of separate renderer
            st.write(f"**Attempts:** {stats['attempts']}")
            st.write(f"**Duration:** {stats['duration']}")
            st.write(f"**Current State:** {stats['state']}")
            st.write(f"**Profanity Count:** {stats['profanity']}")
            st.write(f"**Max Caps %:** {stats['max_caps']:.1f}%")
        
        st.markdown("---")
        st.markdown("### 💩 About")
        st.write("A deliberately unhelpful chatbot.")
        st.write("It understands you perfectly.")
        st.write("It just doesn't care.")


if __name__ == "__main__":
    main()
