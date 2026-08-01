import tempfile
import streamlit as st
from src.chat import answer_question
from src.vector_store import create_vector_store

# Page Configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- ADVANCED UI/UX CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    :root { --muted: #94a3b8; --line: rgba(148, 163, 184, .16); }

    /* Quiet, layered workspace background */
    .stApp {
        background: #070b14;
        background-image: radial-gradient(circle at 78% 0%, rgba(99, 102, 241, .18), transparent 34rem), linear-gradient(145deg, #0b1120 0%, #070b14 58%, #05070c 100%);
        color: #f8fafc;
    }
    
    /* Smooth Container */
    .block-container {
        max-width: 980px;
        padding-top: 1.75rem;
        padding-bottom: 8rem;
    }

    /* Glassmorphism Header */
    .main-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: .9rem 1.15rem;
        background: rgba(15, 23, 42, .62);
        backdrop-filter: blur(18px);
        border: 1px solid var(--line);
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 16px 40px rgba(0,0,0,.18);
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .status-pill {
        padding: 6px 11px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 700;
        background: rgba(34, 197, 94, .1);
        color: #86efac;
        border: 1px solid rgba(34, 197, 94, .25);
        display: flex;
        align-items: center;
        gap: 8px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .status-pill.inactive {
        background: rgba(245, 158, 11, .1);
        color: #fcd34d;
        border-color: rgba(245, 158, 11, .25);
    }

    /* Sleek Sidebar */
    [data-testid="stSidebar"] {
        background: #0a0f1b !important;
        border-right: 1px solid var(--line) !important;
    }
    
    .sidebar-content {
        padding: 1.5rem 1.1rem;
    }

    /* Animated Chat Bubbles */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        margin-bottom: 1rem !important;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stChatMessageContent {
        border-radius: 14px !important;
        padding: .9rem 1.1rem !important;
        line-height: 1.65 !important;
        box-shadow: 0 8px 24px rgba(0,0,0,.12);
        border: 1px solid var(--line) !important;
    }

    /* Assistant Message Style */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stChatMessageContent {
        background: rgba(30, 41, 59, .56) !important;
        backdrop-filter: blur(12px);
        color: #e2e8f0 !important;
    }

    /* User Message Style (Right Aligned & Gradient) */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        flex-direction: row-reverse !important;
    }
    
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stChatMessageContent {
        background: linear-gradient(135deg, #6d5ce7, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        text-align: left;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }

    /* Glass Chat Input */
    .stChatInputContainer {
        background: transparent !important;
        padding-bottom: 3rem !important;
    }
    
    .stChatInputContainer > div {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 24px !important;
        padding: 5px 10px !important;
        box-shadow: 0 -10px 40px rgba(0,0,0,0.4) !important;
    }

    /* File Uploader Customization */
    [data-testid="stFileUploader"] {
        background: rgba(30, 41, 59, 0.3);
        border: 2px dashed rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1rem;
        transition: all 0.3s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1;
        background: rgba(99, 102, 241, 0.05);
    }

    /* Button Styling */
    .stButton button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        letter-spacing: .01em !important;
        transition: all 0.3s !important;
    }

    .eyebrow { color: #a78bfa; font-size: .72rem; font-weight: 700; letter-spacing: .13em; text-transform: uppercase; margin-bottom: .55rem; }
    .welcome { padding: 2.1rem 0 1.25rem; max-width: 650px; }
    .welcome h1 { font-size: clamp(2rem, 5vw, 3.15rem); line-height: 1.04; letter-spacing: -.055em; margin: 0 0 .8rem; }
    .welcome p { color: var(--muted); font-size: 1.02rem; line-height: 1.65; margin: 0; }
    .helper-card { background: rgba(15, 23, 42, .5); border: 1px solid var(--line); border-radius: 14px; padding: 1rem 1.1rem; margin: .5rem 0 1.7rem; color: var(--muted); font-size: .9rem; }
    .helper-card strong { color: #e2e8f0; }
    .sidebar-kicker { color: #a78bfa; font-size: .68rem; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; }
    @media (max-width: 640px) { .block-container { padding-top: 1rem; padding-left: 1rem; padding-right: 1rem; } .main-header { padding: .8rem; } .main-header p { display: none; } .welcome { padding-top: 1.2rem; } }
</style>
""", unsafe_allow_html=True)

# Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = []
if "indexed_file_key" not in st.session_state:
    st.session_state.indexed_file_key = None

# --- GLASS HEADER ---
is_active = st.session_state.indexed_file_key is not None
status_label = "System Online" if is_active else "Standby"
status_class = "status-pill" if is_active else "status-pill inactive"

st.markdown(f"""
    <div class="main-header">
        <div style="display:flex; align-items:center; gap:15px;">
            <div style="background:linear-gradient(135deg, #6366f1, #a855f7); width:40px; height:40px; border-radius:12px; display:flex; align-items:center; justify-content:center; box-shadow:0 0 20px rgba(99, 102, 241, 0.4);">
                <span style="font-size:20px;">🤖</span>
            </div>
            <div>
                <h3 style="margin:0; font-weight:700; letter-spacing:-0.5px;">AI Assistant</h3>
                <p style="margin:0; font-size:10px; color:#94a3b8; font-weight:600; text-transform:uppercase;">Your document workspace</p>
            </div>
        </div>
        <div class="{status_class}">
            <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background-color:currentColor; box-shadow:0 0 10px currentColor;"></span>
            {status_label}
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR DESIGN ---
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("<div class='sidebar-kicker'>Knowledge base</div><h2 style='font-weight:700; color:white; margin:.35rem 0 .45rem;'>Add a document</h2><p style='color:#94a3b8; font-size:.84rem; line-height:1.5; margin-bottom:1.2rem;'>Upload a PDF to give your assistant context.</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type="pdf",
        label_visibility="collapsed"
    )

    if uploaded_file:
        file_bytes = uploaded_file.getvalue()
        file_key = (uploaded_file.name, uploaded_file.size)

        if st.session_state.indexed_file_key != file_key:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file_bytes)
                pdf_path = tmp.name

            with st.status("Indexing document...", expanded=True) as status:
                st.write("Reading and preparing your document")
                create_vector_store(pdf_path)
                status.update(label="Document ready", state="complete", expanded=False)

            st.session_state.indexed_file_key = file_key
            st.session_state.messages = []
            st.rerun()
        else:
            st.success("Document is ready to chat with.")
    
    st.markdown("<div style='margin-top:18rem;'></div>", unsafe_allow_html=True)
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- CHAT ENGINE ---
# Empty state
if not st.session_state.messages:
    st.markdown("""
        <div class="welcome">
            <div class="eyebrow">Document assistant</div>
            <h1>Ask better questions<br>of your documents.</h1>
            <p>Upload a PDF in the sidebar, then explore it with clear, grounded answers.</p>
        </div>
        <div class="helper-card"><strong>Get started:</strong> upload a document, then try “Give me a concise summary” or ask about a specific section.</div>
    """, unsafe_allow_html=True)

# Display historical context
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User query entry
if prompt := st.chat_input("Ask Anything ..."):
    # Immediate UI Feedback
    with st.chat_message("user"):
        st.markdown(prompt)
    
    if not st.session_state.indexed_file_key:
        with st.chat_message("assistant"):
            st.error("Access Denied: Please upload a knowledge source first.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking through your document..."):
                try:
                    response = answer_question(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Neural Error: {str(e)}")
