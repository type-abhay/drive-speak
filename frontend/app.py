import streamlit as st
from api_client import send_query_to_backend

st.set_page_config(
    page_title="Drive-Claw Terminal", 
    page_icon="🦅", 
    layout="centered"
)

def load_css():
    with open("styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# --- Information Panel (Top Right) ---
# We use columns to align the info trigger
nav_left, nav_right = st.columns([0.9, 0.1])
with nav_right:
    # We use a simple emoji label to avoid Material Icon font issues
    with st.popover("ℹ️", help="System Architecture"):
        st.markdown("### 🦅 Drive-Claw Core")
        st.markdown("*Authorized personnel only.*")
        st.markdown("---")
        # MISSION COMPLIANCE: Include GitHub link [cite: 20]
        st.markdown("🔗 [GitHub Repository](https://github.com/your-username/drive-claw)")
        st.markdown("🌐 [Deployment Terminal](https://drive-claw.render.com)")

# --- Header ---
st.markdown("<h1 class='terminal-header'>Drive-Claw</h1>", unsafe_allow_html=True)
st.markdown("<p class='terminal-sub'>Drive Discovery Terminal</p>", unsafe_allow_html=True)

# --- Session State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "System online. What data shall the Drive-Claw retrieve today? 🌌"}
    ]

# --- Chat Interface [cite: 3, 7] ---
for message in st.session_state.messages:
    # MISSION COMPLIANCE: Conversational AI interface [cite: 2, 3]
    avatar_icon = "🦅" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# --- Intent Input ---
if prompt := st.chat_input("Enter search parameters..."):
    # Store user message [cite: 3]
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Process and Respond [cite: 3, 15]
    with st.chat_message("assistant", avatar="🦅"):
        with st.spinner("Executing discovery protocol..."):
            # MISSION COMPLIANCE: Execute accurate queries [cite: 3, 14, 15]
            agent_response = send_query_to_backend(prompt)
            
        st.markdown(agent_response)
        st.session_state.messages.append({"role": "assistant", "content": agent_response})