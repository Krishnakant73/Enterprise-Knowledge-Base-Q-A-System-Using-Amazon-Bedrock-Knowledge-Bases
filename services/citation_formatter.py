from utils.logger import get_logger


# Logger Setup

logger = get_logger(__name__)



# Format Single Citation

def format_single_citation(doc, index=1, preview_chars=400):
    """
    Format one retrieved document into a clean citation block.

    Args:
        doc (dict): Retrieved document dictionary
        index (int): Source number
        preview_chars (int): Number of preview characters

    Returns:
        dict: Clean formatted citation
    """
    try:
        text = doc.get("text", "").strip()
        source = doc.get("source", "Unknown Source")
        metadata = doc.get("metadata", {})

        preview = text[:preview_chars].strip()
        if len(text) > preview_chars:
            preview += "..."

        return {
            "source_number": index,
            "source_name": source,
            "preview": preview,
            "metadata": metadata
        }

    except Exception as e:
        logger.error(f"Error formatting single citation: {str(e)}")
        return {
            "source_number": index,
            "source_name": "Unknown Source",
            "preview": " Unable to display source preview.",
            "metadata": {}
        }



# Format All Citations

def format_citations(docs, preview_chars=400):
    """
    Format a list of retrieved documents into structured citations.

    Args:
        docs (list): Retrieved document dictionaries
        preview_chars (int): Preview character length

    Returns:
        list[dict]: Formatted citations
    """
    if not docs:
        return []

    formatted = []
    for i, doc in enumerate(docs, start=1):
        formatted.append(format_single_citation(doc, index=i, preview_chars=preview_chars))

    return formatted



# Build Citation Text for UI

def build_citation_markdown(docs, preview_chars=400):
    """
    Build markdown string for displaying citations in Streamlit.

    Args:
        docs (list): Retrieved document dictionaries
        preview_chars (int): Preview character length

    Returns:
        str: Markdown formatted citation text
    """
    try:
        citations = format_citations(docs, preview_chars)

        if not citations:
            return "No citations available."

        markdown_blocks = []

        for item in citations:
            block = f"""
###  Source {item['source_number']}
**Document:** `{item['source_name']}`

**Preview:**  
{item['preview']}
"""
            markdown_blocks.append(block.strip())

        return "\n\n---\n\n".join(markdown_blocks)

    except Exception as e:
        logger.error(f"Error building citation markdown: {str(e)}")
        return "⚠️ Failed to build citations."



# Build Compact Citation List

def build_compact_source_list(docs):
    """
    Build a compact list of source names only.

    Args:
        docs (list): Retrieved document dictionaries

    Returns:
        list[str]: List of source labels
    """
    try:
        if not docs:
            return []

        sources = []
        for i, doc in enumerate(docs, start=1):
            source = doc.get("source", "Unknown Source")
            sources.append(f"[Source {i}] {source}")

        return sources

    except Exception as e:
        logger.error(f"Error building compact source list: {str(e)}")
        return []



# Build Inline Citation References

def build_inline_citation_refs(docs):
    """
    Build inline references like [Source 1], [Source 2].

    Args:
        docs (list): Retrieved document dictionaries

    Returns:
        str: Inline source references
    """
    try:
        if not docs:
            return ""

        refs = [f"[Source {i}]" for i in range(1, len(docs) + 1)]
        return " ".join(refs)

    except Exception as e:
        logger.error(f"Error building inline citation refs: {str(e)}")
        return ""