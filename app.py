import streamlit as st

from config.settings import (
    APP_NAME,
    APP_VERSION,
    AWS_REGION,
    KNOWLEDGE_BASE_ID,
    BEDROCK_MODEL_ID,
    TOP_K_RESULTS,
    DEFAULT_PAGE_TITLE,
    DEFAULT_PAGE_ICON,
    DEFAULT_LAYOUT
)

from services.bedrock_kb_service import retrieve_from_kb
from services.answer_generator import generate_answer
from services.citation_formatter import build_citation_markdown, build_compact_source_list
from services.memory_manager import (
    init_memory,
    add_message,
    get_history,
    clear_memory
)

from utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Starting Enterprise Knowledge Assistant app")


# Page Config
st.set_page_config(
    page_title=DEFAULT_PAGE_TITLE,
    page_icon=DEFAULT_PAGE_ICON,
    layout=DEFAULT_LAYOUT,
    initial_sidebar_state="expanded"
)


# Session State Initialization

if "aws_region" not in st.session_state:
    st.session_state.aws_region = AWS_REGION

if "kb_id" not in st.session_state:
    st.session_state.kb_id = KNOWLEDGE_BASE_ID

if "model_id" not in st.session_state:
    st.session_state.model_id = BEDROCK_MODEL_ID

if "top_k" not in st.session_state:
    st.session_state.top_k = TOP_K_RESULTS

if "last_sources" not in st.session_state:
    st.session_state.last_sources = []


# Initialize Chat Memory

init_memory()


# Modern UI CSS

st.markdown("""
<style>

/* GLOBAL - CLEAN CHATBOT THEME */
html, body, [class*="css"] {
    font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
}

.stApp {
    background: #0d1117;
    color: #f8fafc;
}

.block-container {
    max-width: 900px;
    padding-top: 0.5rem !important;
    padding-bottom: 1rem !important;
}

/* ALL TEXT VISIBLE */
p, h1, h2, h3, h4, h5, h6, span, div, label, button {
    color: #f8fafc !important;
}

/* Streamlit markdown text */
[data-testid="stMarkdownContainer"] {
    color: #f8fafc !important;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stMarkdownContainer"] div {
    color: #f8fafc !important;
}

/* All headings */
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-weight: 600;
}

/* Subheaders */
[data-testid="stSubheader"] {
    color: #ffffff !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid rgba(255,255,255,0.1);
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.4rem;
    padding-bottom: 1rem;
}

.sidebar-title {
    font-size: 1.45rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
    color: white;
}

.sidebar-sub {
    font-size: 0.95rem;
    color: #8b949e;
    margin-bottom: 1rem;
    line-height: 1.7;
}

/* CARDS */
.clean-card {
    background: #161b22;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
}

/* BUTTONS */
.stButton > button {
    width: 100%;
    background: #238636;
    color: white !important;
    border: none;
    border-radius: 6px;
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #2ea043;
}

/*  INPUTS */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    border-radius: 6px !important;
    border: 1px solid #30363d !important;
    background: #0d1117 !important;
    color: #f8fafc !important;
}

.stChatInput textarea {
    border-radius: 20px !important;
    border: 1px solid #d0d7de !important;
    background: #ffffff !important;
    color: #24292f !important;
    padding: 12px 16px !important;
    font-size: 1rem !important;
}

/* CHAT INPUT FIX */
[data-testid="stChatInput"] {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
    padding: 8px !important;
    margin-top: 0.6rem !important;
}

[data-testid="stBottomBlockContainer"] {
    background: #0d1117 !important;
}

[data-testid="stChatInputContainer"] {
    background: #0d1117 !important;
}

/*  CHAT MESSAGES */
[data-testid="stChatMessage"] {
    margin-bottom: 1rem !important;
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

[data-testid="stChatMessageContent"] {
    font-size: 1rem;
    line-height: 1.6;
    color: #f8fafc !important;
    background: #21262d;
    padding: 12px 16px;
    border-radius: 12px;
    border: 1px solid #30363d;
}

/* ALERTS */
[data-testid="stAlert"] {
    border-radius: 6px;
    margin-bottom: 1rem !important;
    background: #161b22;
    border: 1px solid #30363d;
}

/* EXPANDERS */
.streamlit-expanderHeader {
    font-weight: 600;
    color: #f8fafc !important;
}

details {
    background: #161b22;
    border-radius: 6px;
    border: 1px solid #30363d;
    padding: 0.5rem;
    margin-bottom: 1rem !important;
}

/* REMOVE SPACERS ONLY */
div[data-testid="stSpacer"] {
    display: none !important;
}

/* CAPTION */
[data-testid="stCaption"] {
    color: #8b949e !important;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 1rem;
}

[data-testid="stFileUploader"] > div {
    color: #f8fafc !important;
}

[data-testid="stFileUploader"] button {
    background: #238636;
    color: white !important;
}

/* HIDE FOOTER / HEADER BG */
footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

</style>
""", unsafe_allow_html=True)


# Sidebar

with st.sidebar:
    st.markdown('<div class="sidebar-title"> System Configuration</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-sub">Configure your AWS Bedrock Knowledge Base settings below.</div>',
        unsafe_allow_html=True
    )

    aws_region_input = st.text_input(
        "AWS Region",
        value=st.session_state.aws_region,
        placeholder="ap-south-2"
    )

    kb_id_input = st.text_input(
        "Knowledge Base ID",
        value=st.session_state.kb_id,
        placeholder="Enter your Bedrock KB ID"
    )

    model_id_input = st.text_input(
        "Bedrock Model ID",
        value=st.session_state.model_id,
        placeholder="amazon.nova-lite-v1:0"
    )

    top_k_input = st.slider(
        "Top-K Retrieval",
        min_value=1,
        max_value=10,
        value=int(st.session_state.top_k)
    )

    if st.button(" Save Settings"):
        st.session_state.aws_region = aws_region_input.strip()
        st.session_state.kb_id = kb_id_input.strip()
        st.session_state.model_id = model_id_input.strip()
        st.session_state.top_k = top_k_input
        st.success("Settings saved successfully")
        st.rerun()

    st.markdown("---")

    if st.button(" Clear Chat"):
        clear_memory()
        st.session_state.last_sources = []
        st.success("Chat cleared")
        st.rerun()

    st.markdown("---")
    st.caption(f"**{APP_NAME}**")
    st.caption(f"Version: {APP_VERSION}")


# Simple Header

st.markdown(f"""
<div style="text-align: center; padding: 0.5rem 0;">
    <h1 style="font-size: 1.8rem; font-weight: 700; color: white; margin: 0;">💬 {APP_NAME}</h1>
    <p style="color: #94a3b8; font-size: 0.9rem; margin: 0.3rem 0 0 0;">Ask questions about your company documents</p>
</div>
""", unsafe_allow_html=True)


# Validation Info

if not st.session_state.kb_id:
    st.warning(" Please add your **Knowledge Base ID** in the sidebar before asking questions.")


# Status

st.caption("🤖 AI Assistant ready")


# Display Chat History

for msg in get_history():
    role = msg["role"]
    content = msg["content"]

    with st.chat_message(role):
        st.markdown(content)


# File Upload Section

with st.expander(" Upload Documents (Optional)"):
    uploaded_files = st.file_uploader(
        "Upload PDFs, TXT, or DOCX files",
        type=['pdf', 'txt', 'docx', 'md'],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    url_input = st.text_input("Or enter a document URL:", placeholder="https://example.com/document.pdf")


# Chat Input

query = st.chat_input("Ask a question about company knowledge...")

# Handle uploaded files
if uploaded_files:
    for file in uploaded_files:
        st.info(f" Uploaded: {file.name}")

if url_input:
    st.info(f" URL added: {url_input}")

if query:
    add_message("user", query)
    logger.info(f"User query received: {query}")

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("🔍 Retrieving relevant knowledge and generating answer..."):
            try:
                if not st.session_state.kb_id:
                    raise ValueError("Knowledge Base ID is missing. Please configure it in the sidebar.")

                
                # Step 1: Retrieve relevant chunks
                
                docs = retrieve_from_kb(
                    query=query,
                    knowledge_base_id=st.session_state.kb_id,
                    region=st.session_state.aws_region,
                    top_k=st.session_state.top_k
                )

                st.session_state.last_sources = docs

                
                # Step 2: Generate grounded answer
                
                answer = generate_answer(
                    query=query,
                    documents=[doc["text"] for doc in docs],
                    model_id=st.session_state.model_id,
                    region=st.session_state.aws_region
                )

                
                # Step 3: Display answer
                
                st.markdown("### ✅ Answer")
                st.markdown(answer)

                
                # Step 4: Compact source list
                
                compact_sources = build_compact_source_list(docs)
                if compact_sources:
                    st.markdown("### 📌 Referenced Sources")
                    for src in compact_sources:
                        st.markdown(f"- {src}")

                add_message("assistant", answer)
                logger.info("Answer generated and displayed successfully")

            except Exception as e:
                logger.error(f"App error: {str(e)}")
                error_message = " Failed to retrieve answer. Please check your AWS configuration, Knowledge Base ID, and permissions."
                st.error(error_message)
                add_message("assistant", error_message)


# Sources Panel

if st.session_state.last_sources:
    with st.expander(" View Sources & Citations"):
        st.markdown(build_citation_markdown(st.session_state.last_sources))