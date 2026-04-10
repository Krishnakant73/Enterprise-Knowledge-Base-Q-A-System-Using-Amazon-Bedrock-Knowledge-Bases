import streamlit as st
from config.settings import MAX_CHAT_HISTORY
from utils.logger import get_logger


# Logger Setup

logger = get_logger(__name__)



# Initialize Chat Memory

def init_memory():
    """
    Initialize Streamlit session-based memory.
    Creates chat history only once per session.
    """
    try:
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            logger.info("Chat memory initialized")
    except Exception as e:
        logger.error(f"Failed to initialize memory: {str(e)}")



# Add Message to Memory

def add_message(role, content):
    """
    Add a new message to chat history.

    Args:
        role (str): 'user' or 'assistant'
        content (str): Message text
    """
    try:
        if "chat_history" not in st.session_state:
            init_memory()

        st.session_state.chat_history.append({
            "role": role,
            "content": content
        })

        trim_history()
        logger.info(f"Added {role} message to memory")

    except Exception as e:
        logger.error(f"Failed to add message: {str(e)}")



# Get Full Chat History

def get_history():
    """
    Return current chat history.

    Returns:
        list: Chat history list
    """
    try:
        if "chat_history" not in st.session_state:
            init_memory()

        return st.session_state.chat_history

    except Exception as e:
        logger.error(f"Failed to get history: {str(e)}")
        return []



# Get Only Recent History

def get_recent_history(limit=MAX_CHAT_HISTORY):
    """
    Return only the most recent chat turns.

    Args:
        limit (int): Number of recent messages to keep

    Returns:
        list: Recent history
    """
    try:
        history = get_history()
        return history[-limit:]

    except Exception as e:
        logger.error(f"Failed to get recent history: {str(e)}")
        return []



# Trim Chat History

def trim_history(limit=MAX_CHAT_HISTORY):
    """
    Keep only the latest N messages to avoid oversized session memory.

    Args:
        limit (int): Max number of messages to keep
    """
    try:
        if "chat_history" not in st.session_state:
            init_memory()

        if len(st.session_state.chat_history) > limit:
            st.session_state.chat_history = st.session_state.chat_history[-limit:]
            logger.info(f"Trimmed chat history to last {limit} messages")

    except Exception as e:
        logger.error(f"Failed to trim history: {str(e)}")



# Clear Chat History

def clear_memory():
    """
    Clear all chat history from current session.
    """
    try:
        st.session_state.chat_history = []
        logger.info("Chat memory cleared")

    except Exception as e:
        logger.error(f"Failed to clear memory: {str(e)}")



# Export History as Prompt Context

def history_to_prompt(limit=MAX_CHAT_HISTORY):
    """
    Convert recent chat history into prompt-friendly text.

    Useful if you want to pass prior conversation into the LLM prompt.

    Args:
        limit (int): Number of recent messages to include

    Returns:
        str: Prompt-ready conversation history
    """
    try:
        recent_history = get_recent_history(limit)

        if not recent_history:
            return ""

        lines = []
        for msg in recent_history:
            role = msg["role"].capitalize()
            content = msg["content"].strip()
            lines.append(f"{role}: {content}")

        return "\n".join(lines)

    except Exception as e:
        logger.error(f"Failed to convert history to prompt: {str(e)}")
        return ""