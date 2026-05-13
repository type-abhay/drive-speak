import streamlit as st
from api_client import send_query_to_backend

st.set_page_config(
    page_title="DriveClaw Terminal", 
    page_icon="assets/logo.png",
    layout="centered"
)

def load_css():
    with open("styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# --- Information Panel (Top Right) ---
nav_left, nav_right = st.columns([0.9, 0.1])
with nav_right:
    with st.popover(":material/info:", help="Disclaimer"):
        st.markdown("###  Drive-Claw Disclaimers")
        st.markdown("<div class='system-warning'>" 
        "Please be mindful while testing; <br>"
        "running on a <b>FREE GEMINI API KEY</b>."
        "</div>",unsafe_allow_html=True)
        st.markdown("<div class='system-warning'>"
        "Running of <b>Render's Free Tier</b> and free instances  after 15 minutes of inactivity, meaning the <b>very first request</b><br>"
        "<b> after a pause</b> will take about <b>40–50s</b> to wake the server up."
        "</div>",unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<div class='system-warning'><b><a href='https://github.com/type-abhay/drive-speak/'>Github</a></b></div>",unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 class='terminal-header'>Drive-Claw</h1>", unsafe_allow_html=True)
st.markdown("<p class='terminal-sub'>Drive Discovery Terminal</p>", unsafe_allow_html=True)

# --- Session State Management ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "System online. What data shall the Drive-Claw retrieve today? 🌌"}
    ]

# start
FAVICON_PATH = "assets/logo.png"
for message in st.session_state.messages:
    avatar_path = FAVICON_PATH if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar_path):
        st.markdown(message["content"])

# --- Intent Input ---
if prompt := st.chat_input("Enter search parameters..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Process and Respond
    with st.chat_message("assistant", avatar=FAVICON_PATH):
        with st.spinner("Executing discovery protocol..."):
            agent_response = send_query_to_backend(prompt)
            
        st.markdown(agent_response)
        st.session_state.messages.append({"role": "assistant", "content": agent_response})