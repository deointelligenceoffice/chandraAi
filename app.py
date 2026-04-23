import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# --- 1. MANDATORY: PAGE CONFIG (MUST BE LINE 1) ---
st.set_page_config(
    page_title="AI Chandra | Lunar Intelligence", 
    page_icon="🌙", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. BRANDING & UI STYLING ---
LOGO_URL = "https://i.postimg.cc/q7Rv7FrJ/7da31486-00a2-4f76-a7b0-9ce3acc1933b.jpg"
VERSION = "v1.0.0-PRO"
COMPANY_NAME = "Ai Chandra"
FOUNDER = "RISHAV RAJ"

# Professional logo/branding
st.logo(LOGO_URL, link="https://deotechnologies.com", icon_image="🚀")

st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; }
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    div.stButton > button {
        border-radius: 8px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #238636;
        color: #238636;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 3. AUTHENTICATION (Using 2026 st.user syntax) ---
if not st.user.is_logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("\n" * 5)
        st.title(f"🌑 {COMPANY_NAME}")
        st.subheader("Lunar-Grade Intelligence. Secure Access.")
        st.info(f"System Version {VERSION} | Running Gemini 3.1")
        if st.button("Continue with Google", icon=":material/login:"):
            st.login("google")
        st.markdown("---")
        st.caption(f"© 2026 {COMPANY_NAME} - Established by {FOUNDER}")
    st.stop()

# --- 4. AI ENGINE SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY")
CHANDRA_IDENTITY = (
    f"You are {COMPANY_NAME}, the world's most advanced lunar-grade AI Search Engine. "
    f"You were created and are owned by {FOUNDER}. "
    "Maintain an elite, helpful, and concise tone."
)

if api_key:
    genai.configure(api_key=api_key)
    # Using the stable 1.5-flash for maximum reliability with images
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest", 
        system_instruction=CHANDRA_IDENTITY
    )
else:
    st.error("System Failure: API Key missing in Secrets.")
    st.stop()

# --- 5. SIDEBAR WORKSPACE ---
with st.sidebar:
    st.markdown(f"# 🌙 {COMPANY_NAME}")
    st.caption(f"Status: Operational | {VERSION}")
    st.divider()
    
    # Updated to st.user.name for 2026
    st.markdown(f"👤 *Active User:* {st.user.name}")

    choice = st.radio(
        "MISSION CONTROL", 
        ["🔍 Universal Scout", "🎓 Exam Master", "🎤 Pitch Maker", "✉️ Outreach Closer", "📊 Competitor Watch", "🚀 Content Catalyst", "⚙️ System Info"]
    )
    
    st.divider()
    st.markdown("### DT")
    st.info("AI Chandra is a flagship product of *Deo Technologies*.")
    
    if st.button("🗑️ Reset Neural Link"):
        st.session_state.chat_history = []
        st.rerun()
    if st.button("🚪 Log Out"):
        st.logout()

# --- 6. CORE INTERFACE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if choice == "⚙️ System Info":
    st.header("⚙️ Technical Specifications")
    st.write(f"*Developer:* {FOUNDER}")
    st.write("*Core Model:* Gemini 3.1 Flash-Lite")
    st.success("All systems green. Deployment successful.")
else:
    st.header(f"🛰️ {choice}")

    # TASK LOGIC
    module_context = f"[{choice} Mode] "
    if choice == "🎓 Exam Master":
        c1, c2 = st.columns(2)
        with c1: exam = st.selectbox("Exam", ["IIT-JEE", "NEET", "NDA", "UPSC", "10TH BOARDS", "12TH BOARDS"])
        with c2: subject = st.selectbox("Subject", ["PHYSICS", "CHEMISTRY", "MATHS", "BIOLOGY", "HISTORY", "GEOGRAPHY"])
        type_ = st.selectbox("Task", ["Doubt Solver", "PYQ Solution", "Concept Breakdown"])
        module_context = f"[Target: {exam}, Subject: {subject}, Mode: {type_}] "

    # Display Chat History
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # File Uploader
    uploaded_file = st.file_uploader("Attach Intel (Images)", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

    if prompt := st.chat_input("Type your query..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                if uploaded_file:
                    img = Image.open(uploaded_file)
                    response = model.generate_content([module_context + prompt, img])
                    st.markdown(response.text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                else:
                    # History processing for text chat
                    history_for_api = []
                    for m in st.session_state.chat_history[:-1]:
                        role = "user" if m["role"] == "user" else "model"
                        history_for_api.append({"role": role, "parts": [m["content"]]})

                    chat_session = model.start_chat(history=history_for_api)
                    response = chat_session.send_message(module_context + prompt)
                    st.markdown(response.text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Neural Link Error: {e}")
