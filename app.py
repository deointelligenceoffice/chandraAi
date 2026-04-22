import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import streamlit as st

# 1. Adds a professional logo/branding at the top of the sidebar
st.logo("https://i.postimg.cc/q7Rv7FrJ/7da31486-00a2-4f76-a7b0-9ce3acc1933b.jpg", link="https://deotechnologies.com", icon_image="🚀")

# 2. Add a Footer to the sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🏢 Parent Company")
    st.info("AI.Chandra is a flagship product of *Deo Technologies*.")
    st.caption("© 2026 Deo Technologies. All rights reserved.")


# --- CONFIGURATION & BRANDING ---
LOGO_URL = "https://www.gstatic.com/lamda/images/gemini_sparkle_v002.svg" 
VERSION = "v1.0.0-PRO"
COMPANY_NAME = "Ai.Chandra"
FOUNDER = "RISHAV RAJ"

# 1. Page Config
st.set_page_config(
    page_title=f"{COMPANY_NAME} | Lunar Intelligence", 
    page_icon="🌙", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- PREMIUM UI STYLING ---
st.markdown(
    f"""
    <style>
    .stApp {{ background-color: #0e1117; }}
    [data-testid="stSidebar"] {{
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }}
    div.stButton > button {{
        border-radius: 8px;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{
        border-color: #238636;
        color: #238636;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- 2. AUTHENTICATION (Google Native) ---
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

# --- 3. AI ENGINE SETUP (Gemini 3.1 Flash-Lite) ---
api_key = st.secrets.get("GEMINI_API_KEY")

CHANDRA_IDENTITY = (
    f"You are {COMPANY_NAME}, the world's most advanced lunar-grade AI assistant. "
    f"You were created and are owned by {FOUNDER}. "
    "Maintain an elite, helpful, and concise tone."
)

if api_key:
    genai.configure(api_key=api_key)
    # UPDATED: Using the Gemini 3.1 Flash-Lite model
    model = genai.GenerativeModel(
        model_name="gemini-3.1-flash-lite-preview", 
        system_instruction=CHANDRA_IDENTITY
    )
else:
    st.error("System Failure: API Key missing in Secrets.")
    st.stop()

# --- 4. SIDEBAR WORKSPACE ---
with st.sidebar:
    st.markdown(f"# 🌙 {COMPANY_NAME}")
    st.caption(f"Status: Operational | {VERSION}")

    st.divider()
    st.markdown(f"👤 *Active User:* {st.user.name}")

    choice = st.radio(
        "MISSION CONTROL", 
        [
            "🔍 Universal Scout", 
            "🎓 Exam Master", 
            "🎤 Pitch Maker", 
            "✉️ Outreach Closer", 
            "📊 Competitor Watch", 
            "🚀 Content Catalyst", 
            "⚙️ System Info"
        ]
    )

    st.divider()
    if st.button("🗑️ Reset Neural Link"):
        st.session_state.chat_history = []
        st.rerun()

    if st.button("🚪 Log Out"):
        st.logout()

# --- 5. CORE INTERFACE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if choice == "⚙️ System Info":
    st.header("⚙️ Technical Specifications")
    st.write(f"*Developer:* {FOUNDER}")
    st.write("*Core Model:* Gemini 3.1 Flash-Lite (2026 Elite)")
    st.write("*License:* Apache 2.0 Professional")
    st.success("All systems green. Deployment successful.")

else:
    st.header(f"🛰️ {choice}")

    # TASK LOGIC (Doubt Solver added here)
    if choice == "🎓 Exam Master":
        c1, c2 ,c3 = st.columns(3)
        with c1: exam = st.selectbox("Exam", ["IIT-JEE", "NEET", "NDA", "UPSC", "10TH BOARDS", "12TH BOARDS"])
        with c1: subject = st.selectbox("Exam", ["PHYSICS", "CHEMISTRY", "MATHS", "BIOLOGY" , "REASONING", "CURRENT AFFAIRS", "HISTORY", "GEOGRAPHY" , "CIVICS", "INDIAN POLITY", "INDIAN ECONOMY", "COMPUTER APPLICATIONS"])
        with c3: type_ = st.selectbox("Task", ["Doubt Solver", "PYQ Solution", "Concept Breakdown", "Mock Question"])
        module_context = f"[Target: {exam}, Mode: {type_}] "

    elif choice == "🎤 Pitch Maker":
        pitch_type = st.selectbox("Pitch Deck Focus", ["Seed Funding", "Client Proposal", "Product Launch"])
        module_context = f"[Business Mode: Generating a {pitch_type} pitch] "

    else:
        module_context = f"[{choice} Mode] "

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

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
                    history_for_api = []
                    for m in st.session_state.chat_history[:-1]:
                        role = "user" if m["role"] == "user" else "model"
                        history_for_api.append({"role": role, "parts": [m["content"]]})

                    chat_session = model.start_chat(history=history_for_api)
                    response = chat_session.send_message(module_context + prompt, stream=True)

                    full_response = ""
                    placeholder = st.empty()
                    for chunk in response:
                        full_response += chunk.text
                        placeholder.markdown(full_response + "▌")
                    placeholder.markdown(full_response)

                    st.session_state.chat_history.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"Neural Link Error: {e}")
