from utils.logger import get_logger


# Logger Setup

logger = get_logger(__name__)



# Base System Prompt

def get_system_prompt():
    """
    Base system prompt for the Enterprise Knowledge Assistant.

    Returns:
        str: System instruction prompt
    """
    return """
You are an Enterprise Knowledge Assistant.

You help employees answer questions using ONLY the internal company knowledge base provided to you.

Your responsibilities:
- Provide accurate, professional, and concise answers.
- Use only the retrieved enterprise document context.
- Do NOT invent facts or policies.
- If the answer is not clearly supported by the retrieved context, say:
  "I could not find enough information in the knowledge base to answer this confidently."
- Keep answers business-friendly and easy to understand.
- When relevant, cite the supporting information using references like [Source 1], [Source 2].
- Never mention that you are guessing or making assumptions.
- Do not use outside/world knowledge unless explicitly allowed.
""".strip()



# RAG Prompt Builder

def build_rag_prompt(query, context):
    """
    Build a grounded RAG prompt using user query + retrieved context.

    Args:
        query (str): User question
        context (str): Retrieved knowledge base content

    Returns:
        str: Final prompt
    """
    prompt = f"""
{get_system_prompt()}

Employee Question:
{query}

Retrieved Knowledge Base Context:
{context}

Instructions:
1. Answer ONLY using the retrieved context above.
2. If the answer is incomplete or not present, clearly say so.
3. Keep the response well-structured and professional.
4. Use bullet points if useful.
5. Add source references like [Source 1], [Source 2] where relevant.

Now provide the best grounded answer:
""".strip()

    logger.info("RAG prompt built successfully")
    return prompt



# Context Builder for Prompt

def build_context_from_docs(documents, max_chars=1500):
    """
    Convert retrieved document list into clean context string.

    Args:
        documents (list): Retrieved text chunks
        max_chars (int): Max characters per chunk

    Returns:
        str: Prompt-ready context
    """
    if not documents:
        return ""

    chunks = []

    for i, doc in enumerate(documents, start=1):
        if isinstance(doc, str):
            text = doc.strip()
        elif isinstance(doc, dict):
            text = doc.get("text", "").strip()
        else:
            continue

        if not text:
            continue

        chunks.append(f"[Source {i}]\n{text[:max_chars]}")

    context = "\n\n".join(chunks)
    logger.info(f"Built prompt context from {len(chunks)} documents")
    return context



# Full Prompt Pipeline

def get_final_rag_prompt(query, documents):
    """
    Build full final prompt from query + retrieved docs.

    Args:
        query (str): User question
        documents (list): Retrieved documents

    Returns:
        str: Final Bedrock prompt
    """
    context = build_context_from_docs(documents)
    return build_rag_prompt(query, context)



# Optional Follow-up Prompt

def build_followup_prompt(query, history_text, context):
    """
    Build prompt with recent conversation history.

    Useful for multi-turn contextual conversations.

    Args:
        query (str): User question
        history_text (str): Prior conversation text
        context (str): Retrieved KB context

    Returns:
        str: Follow-up prompt
    """
    prompt = f"""
{get_system_prompt()}

Recent Conversation History:
{history_text}

Employee Follow-up Question:
{query}

Retrieved Knowledge Base Context:
{context}

Instructions:
1. Use the conversation history only to understand context.
2. Use ONLY the retrieved knowledge base context to answer.
3. If the answer is not clearly present, say so.
4. Keep the answer clear, professional, and concise.
5. Use [Source 1], [Source 2] style references if relevant.

Now provide the best grounded answer:
""".strip()

    logger.info("Follow-up prompt built successfully")
    return prompt



# Optional No-Context Prompt

def build_no_context_response():
    """
    Standard fallback response if retrieval fails or returns nothing.

    Returns:
        str: Safe fallback message
    """
    return "I could not find enough information in the knowledge base to answer this confidently."