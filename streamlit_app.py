import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import time

# ============== CONFIGURATION ==============
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== PROFESSIONAL COLOR BRANDING ==============
COLORS = {
    "primary": "#6366F1",        # Indigo
    "primary_dark": "#4F46E5",   # Darker indigo
    "secondary": "#10B981",      # Emerald
    "accent": "#F59E0B",         # Amber
    "background": "#0F172A",     # Dark slate
    "surface": "#1E293B",        # Slate surface
    "surface_light": "#334155",  # Lighter slate
    "text_primary": "#F8FAFC",   # White-ish
    "text_secondary": "#94A3B8", # Muted gray
    "user_msg": "#312E81",       # Indigo for user
    "ai_msg": "#1E293B",         # Slate for AI
    "border": "#475569",         # Border color
    "success": "#22C55E",        # Green
    "warning": "#EAB308",        # Yellow
    "error": "#EF4444",          # Red
}

# ============== CUSTOM CSS ==============
st.markdown(f"""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global Styles */
    .stApp {{
        background: linear-gradient(135deg, {COLORS['background']} 0%, #1a1a2e 100%);
        font-family: 'Inter', sans-serif;
    }}

    /* Hide default Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display: none;}}

    /* Header Styling */
    .header-container {{
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(99, 102, 241, 0.3);
    }}

    .header-title {{
        font-size: 2rem;
        font-weight: 700;
        color: {COLORS['text_primary']};
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .header-subtitle {{
        color: rgba(255,255,255,0.8);
        font-size: 0.95rem;
        margin-top: 0.5rem;
    }}

    /* Sidebar Styling */
    .sidebar-content {{
        background: {COLORS['surface']};
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }}

    .sidebar-title {{
        color: {COLORS['text_primary']};
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .sidebar-stat {{
        background: {COLORS['surface_light']};
        padding: 0.75rem 1rem;
        border-radius: 10px;
        margin-bottom: 0.75rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .sidebar-stat-label {{
        color: {COLORS['text_secondary']};
        font-size: 0.85rem;
    }}

    .sidebar-stat-value {{
        color: {COLORS['primary']};
        font-weight: 600;
        font-size: 0.9rem;
    }}

    /* Chat Message Styling */
    .chat-message {{
        padding: 1rem 1.25rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        max-width: 85%;
        line-height: 1.6;
        animation: fadeIn 0.3s ease-out;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .user-message {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
        color: {COLORS['text_primary']};
        margin-left: auto;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
    }}

    .ai-message {{
        background: {COLORS['surface']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        margin-right: auto;
        border-bottom-left-radius: 4px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }}

    .message-avatar {{
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-right: 10px;
        font-size: 1.1rem;
    }}

    .user-avatar {{
        background: {COLORS['secondary']};
    }}

    .ai-avatar {{
        background: {COLORS['primary']};
    }}

    /* Input Styling */
    .input-container {{
        background: {COLORS['surface']};
        border-radius: 16px;
        padding: 1rem;
        border: 2px solid {COLORS['border']};
        transition: all 0.3s ease;
    }}

    .input-container:focus-within {{
        border-color: {COLORS['primary']};
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
    }}

    /* Button Styling */
    .stButton > button {{
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(99, 102, 241, 0.4);
    }}

    .clear-btn > button {{
        background: linear-gradient(90deg, {COLORS['error']} 0%, #DC2626 100%);
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }}

    .clear-btn > button:hover {{
        box-shadow: 0 6px 25px rgba(239, 68, 68, 0.4);
    }}

    /* Footer Styling */
    .footer-container {{
        background: {COLORS['surface']};
        padding: 1rem 2rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 2rem;
    }}

    .footer-text {{
        color: {COLORS['text_secondary']};
        font-size: 0.85rem;
    }}

    .footer-link {{
        color: {COLORS['primary']};
        text-decoration: none;
    }}

    /* Turn Counter */
    .turn-counter {{
        background: {COLORS['warning']};
        color: #1a1a1a;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-top: 0.5rem;
    }}

    .turn-counter.warning {{
        background: {COLORS['error']};
        color: white;
    }}

    /* Divider */
    .custom-divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent, {COLORS['border']}, transparent);
        margin: 1.5rem 0;
    }}

    /* Loading Animation */
    .typing-indicator {{
        display: inline-flex;
        gap: 4px;
    }}

    .typing-dot {{
        width: 8px;
        height: 8px;
        background: {COLORS['text_secondary']};
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out;
    }}

    .typing-dot:nth-child(1) {{ animation-delay: -0.32s; }}
    .typing-dot:nth-child(2) {{ animation-delay: -0.16s; }}

    @keyframes bounce {{
        0%, 80%, 100% {{ transform: scale(0.6); opacity: 0.5; }}
        40% {{ transform: scale(1); opacity: 1; }}
    }}

    /* Session Info */
    .session-info {{
        background: linear-gradient(135deg, {COLORS['primary']}20 0%, {COLORS['secondary']}20 100%);
        border: 1px solid {COLORS['primary']}40;
        border-radius: 12px;
        padding: 1rem;
    }}
</style>
""", unsafe_allow_html=True)

# ============== LLM CONFIGURATION ==============
@st.cache_resource
def get_llm():
    return ChatOllama(
        model="qwen2.5-coder:3b",
        temperature=0.7
    )

def get_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI Assistant"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}")
    ])

def get_chain():
    return get_prompt() | get_llm() | StrOutputParser()

# ============== SESSION STATE ==============
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "turns_used" not in st.session_state:
    st.session_state.turns_used = 0

MAX_TURNS = 6

# ============== HELPER FUNCTIONS ==============
def clear_chat():
    st.session_state.chat_history = []
    st.session_state.messages = []
    st.session_state.turns_used = 0
    st.rerun()

def get_turns_remaining():
    return MAX_TURNS - st.session_state.turns_used

def is_low_on_turns():
    return get_turns_remaining() <= 2

# ============== SIDEBAR ==============
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-content">
        <div class="sidebar-title">
            <span>⚙️</span> Chat Settings
        </div>
        <div class="sidebar-stat">
            <span class="sidebar-stat-label">🤖 Model</span>
            <span class="sidebar-stat-value">qwen2.5-coder:3b</span>
        </div>
        <div class="sidebar-stat">
            <span class="sidebar-stat-label">💬 Conversations</span>
            <span class="sidebar-stat-value">{st.session_state.turns_used}/{MAX_TURNS}</span>
        </div>
        <div class="sidebar-stat">
            <span class="sidebar-stat-label">📊 Total Messages</span>
            <span class="sidebar-stat-value">{len(st.session_state.messages)}</span>
        </div>
        <div class="sidebar-stat">
            <span class="sidebar-stat-label">⏱️ Temperature</span>
            <span class="sidebar-stat-value">0.7</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(f"""
    <div class="sidebar-content">
        <div class="sidebar-title">
            <span>📋</span> Quick Actions
        </div>
    """, unsafe_allow_html=True)

    if st.button("🗑️ Clear Chat History", use_container_width=True, key="clear_btn"):
        clear_chat()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Model info card
    st.markdown(f"""
    <div class="session-info">
        <div class="sidebar-title" style="margin-bottom: 0.5rem;">
            <span>ℹ️</span> About
        </div>
        <p style="color: {COLORS['text_secondary']}; font-size: 0.85rem; margin: 0;">
            This chatbot uses <strong style="color: {COLORS['primary']}">LangChain</strong>
            with <strong style="color: {COLORS['secondary']}">Ollama</strong>
            for local AI inference.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============== MAIN HEADER ==============
st.markdown(f"""
<div class="header-container">
    <h1 class="header-title">
        <span>🤖</span>
        AI Assistant
    </h1>
    <p class="header-subtitle">
        Powered by LangChain + Ollama • Start a conversation below
    </p>
</div>
""", unsafe_allow_html=True)

# ============== CHAT CONTAINER ==============
chat_container = st.container()

with chat_container:
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <span class="message-avatar user-avatar">👤</span>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message ai-message">
                <span class="message-avatar ai-avatar">🤖</span>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)

    # Show turn warning if low on turns
    if is_low_on_turns() and st.session_state.turns_used > 0:
        remaining = get_turns_remaining()
        warning_class = "warning" if remaining <= 1 else ""
        st.markdown(f"""
        <div class="turn-counter {warning_class}">
            ⚠️ Only {remaining} turn(s) left! Consider clearing chat for new context.
        </div>
        """, unsafe_allow_html=True)

    # Show max turns message
    if st.session_state.turns_used >= MAX_TURNS:
        st.markdown(f"""
        <div class="chat-message ai-message" style="border-color: {COLORS['error']};">
            <span class="message-avatar ai-avatar">⚠️</span>
            <strong>Context window is full!</strong><br><br>
            The AI may not follow our previous conversation properly.<br>
            Please click <strong>"Clear Chat History"</strong> in the sidebar to start fresh.
        </div>
        """, unsafe_allow_html=True)

# ============== CHAT INPUT ==============
st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])

    with col1:
        user_input = st.text_input(
            "Type your message...",
            placeholder="Ask me anything...",
            label_visibility="collapsed",
            key="chat_input"
        )

    with col2:
        submit_button = st.form_submit_button(
            "Send ➤",
            use_container_width=True
        )

# ============== HANDLE SUBMISSION ==============
if submit_button and user_input.strip():
    if st.session_state.turns_used >= MAX_TURNS:
        st.error("Maximum conversation turns reached. Please clear the chat to continue.")
    else:
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input.strip()
        })

        # Show typing indicator
        with st.spinner("🤖 AI is thinking..."):
            try:
                # Get response from chain
                chain = get_chain()
                response = chain.invoke({
                    "question": user_input.strip(),
                    "chat_history": st.session_state.chat_history
                })

                # Add AI response
                st.session_state.messages.append({
                    "role": "ai",
                    "content": response
                })

                # Update chat history for LangChain
                st.session_state.chat_history.append(
                    HumanMessage(content=user_input.strip())
                )
                st.session_state.chat_history.append(
                    AIMessage(content=response)
                )

                # Increment turn counter
                st.session_state.turns_used += 1

                # Rerun to show new messages
                st.rerun()

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.messages.pop()

# ============== FOOTER ==============
st.markdown(f"""
<div class="custom-divider"></div>
<div class="footer-container">
    <p class="footer-text">
        🚀 Built with <strong>Streamlit</strong> + <strong>LangChain</strong> + <strong>Ollama</strong>
    </p>
    <p class="footer-text" style="margin-top: 0.5rem; opacity: 0.7;">
        © 2024 AI Chatbot • Local & Private
    </p>
</div>
""", unsafe_allow_html=True)
