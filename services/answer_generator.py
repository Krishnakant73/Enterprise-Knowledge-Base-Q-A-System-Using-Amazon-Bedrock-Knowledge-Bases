import boto3
import json
from config.settings import (
    TEMPERATURE,
    MAX_OUTPUT_TOKENS,
    MAX_CONTEXT_CHARS
)
from utils.logger import get_logger


# Logger Setup

logger = get_logger(__name__)



# Build Context from Retrieved Docs

def build_context(documents, max_chars=MAX_CONTEXT_CHARS):
    """
    Convert retrieved document chunks into a clean prompt context.
    
    Args:
        documents (list): List of retrieved text chunks
        max_chars (int): Max characters per chunk
    
    Returns:
        str: Combined context string
    """
    if not documents:
        return ""

    cleaned_chunks = []

    for i, doc in enumerate(documents, start=1):
        if not isinstance(doc, str):
            continue

        chunk = doc.strip()
        if not chunk:
            continue

        cleaned_chunks.append(f"[Source {i}]\n{chunk[:max_chars]}")

    return "\n\n".join(cleaned_chunks)



# Build Final Prompt

def build_rag_prompt(query, context):
    """
    Builds a grounded enterprise RAG prompt.
    
    Args:
        query (str): User question
        context (str): Retrieved knowledge base context
    
    Returns:
        str: Prompt for Bedrock model
    """
    return f"""
You are an enterprise knowledge assistant.

Your job is to answer employee questions using ONLY the provided internal company knowledge base context.

Rules:
1. Answer ONLY from the provided context.
2. Do NOT make up facts.
3. If the answer is not clearly available in the context, say:
   "I could not find enough information in the knowledge base to answer this confidently."
4. Keep the answer professional, concise, and easy to understand.
5. If possible, organize the answer using bullet points or short sections.
6. Mention source references like [Source 1], [Source 2] when relevant.

Employee Question:
{query}

Retrieved Knowledge Base Context:
{context}

Now provide the best grounded answer:
""".strip()



# Parse Bedrock Response Safely

def parse_bedrock_response(response_body):
    """
    Safely parse Bedrock model response.

    Args:
        response_body (dict): Decoded Bedrock response JSON

    Returns:
        str: Extracted answer text
    """
    try:
        # Amazon Nova / Titan-style
        if "output" in response_body and "message" in response_body["output"]:
            content = response_body["output"]["message"].get("content", [])
            if content and isinstance(content, list):
                texts = [item.get("text", "") for item in content if "text" in item]
                return "\n".join(texts).strip()

        # Anthropic Claude-style fallback
        if "content" in response_body:
            content = response_body["content"]
            if isinstance(content, list):
                texts = [item.get("text", "") for item in content if "text" in item]
                return "\n".join(texts).strip()

        # Generic fallback
        if "completion" in response_body:
            return response_body["completion"].strip()

        return " No valid answer was returned by the model."

    except Exception as e:
        logger.error(f"Failed to parse Bedrock response: {str(e)}")
        return " Failed to parse model response."



# Generate Answer using Bedrock Model

def generate_answer(query, documents, model_id, region):
    """
    Generate grounded answer using retrieved knowledge base documents.

    Args:
        query (str): User question
        documents (list): Retrieved text chunks
        model_id (str): Bedrock model ID
        region (str): AWS region

    Returns:
        str: Final grounded answer
    """
    try:
        if not documents:
            logger.warning("No documents retrieved from knowledge base")
            return "I could not find enough information in the knowledge base to answer this confidently."

        context = build_context(documents)
        prompt = build_rag_prompt(query, context)

        logger.info("Initializing Bedrock Runtime client for answer generation")
        client = boto3.client("bedrock-runtime", region_name=region)

        # Amazon Nova request format
        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"text": prompt}
                    ]
                }
            ],
            "inferenceConfig": {
                "temperature": TEMPERATURE,
                "max_new_tokens": MAX_OUTPUT_TOKENS
            }
        }

        logger.info("Invoking Bedrock model for grounded answer")
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        response_body = json.loads(response["body"].read())
        answer = parse_bedrock_response(response_body)

        logger.info("Answer generated successfully")
        return answer

    except Exception as e:
        logger.error(f"Answer generation failed: {str(e)}")
        return " Failed to generate an answer from the retrieved knowledge base content."