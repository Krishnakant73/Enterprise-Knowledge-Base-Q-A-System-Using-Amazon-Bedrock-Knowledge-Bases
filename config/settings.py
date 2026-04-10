import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# App Metadata

APP_NAME = "Enterprise Knowledge Assistant"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = " RAG Q&A system using Amazon Bedrock Knowledge Bases"


# AWS / Bedrock Configuration

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Bedrock Knowledge Base ID
KNOWLEDGE_BASE_ID = os.getenv("HBC7PRIQ7H",)

# Bedrock Model ID for answer generation
# Recommended:
# amazon.nova-lite-v1:0
# anthropic.claude-3-haiku-20240307-v1:0
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0")


# Retrieval Settings
#
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", 3))

# Maximum number of chat turns to keep in memory
MAX_CHAT_HISTORY = int(os.getenv("MAX_CHAT_HISTORY", 10))

# Max characters from each retrieved document chunk
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", 1500))


# UI Defaults

DEFAULT_PAGE_TITLE = "Enterprise Knowledge Assistant"
DEFAULT_PAGE_ICON = "💬"
DEFAULT_LAYOUT = "wide"


# Logging

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE = os.getenv("LOG_FILE", "app.log")


# Prompt / Response Controls

TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", 1024))


# Validation Helper

def validate_settings():
    """
    Validates required settings before app startup.
    Raises ValueError if required settings are missing.
    """
    errors = []

    if not KNOWLEDGE_BASE_ID:
        errors.append("KNOWLEDGE_BASE_ID is missing in environment variables.")

    if not AWS_REGION:
        errors.append("AWS_REGION is missing in environment variables.")

    if not BEDROCK_MODEL_ID:
        errors.append("BEDROCK_MODEL_ID is missing in environment variables.")

    if errors:
        raise ValueError(" | ".join(errors))