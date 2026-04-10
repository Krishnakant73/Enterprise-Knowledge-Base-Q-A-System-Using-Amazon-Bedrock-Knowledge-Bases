import boto3
from botocore.exceptions import BotoCoreError, ClientError
from utils.logger import get_logger


# Logger Setup

logger = get_logger(__name__)



# Create Bedrock Agent Runtime Client

def get_bedrock_kb_client(region):
    """
    Create Bedrock Agent Runtime client.

    Args:
        region (str): AWS region

    Returns:
        boto3 client
    """
    try:
        client = boto3.client("bedrock-agent-runtime", region_name=region)
        logger.info(f"Bedrock KB client initialized for region: {region}")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Bedrock KB client: {str(e)}")
        raise



# Extract Retrieval Results Safely

def parse_retrieval_results(results):
    """
    Parse Bedrock Knowledge Base retrieval results into structured format.

    Args:
        results (list): Raw retrieval results

    Returns:
        list[dict]: Cleaned list of retrieved chunks
    """
    parsed_docs = []

    if not results:
        return parsed_docs

    for item in results:
        try:
            text = item.get("content", {}).get("text", "").strip()
            location = item.get("location", {})
            metadata = item.get("metadata", {})

            # Try to extract source URI or file name
            source = "Unknown Source"

            if "s3Location" in location:
                source = location["s3Location"].get("uri", "Unknown Source")
            elif "webLocation" in location:
                source = location["webLocation"].get("url", "Unknown Source")
            elif metadata.get("source"):
                source = metadata.get("source")

            if text:
                parsed_docs.append({
                    "text": text,
                    "source": source,
                    "metadata": metadata
                })

        except Exception as e:
            logger.warning(f"Skipping malformed retrieval item: {str(e)}")
            continue

    return parsed_docs



# Retrieve from Bedrock Knowledge Base

def retrieve_from_kb(query, knowledge_base_id, region, top_k=3):
    """
    Retrieve relevant document chunks from Amazon Bedrock Knowledge Base.

    Args:
        query (str): User question
        knowledge_base_id (str): Bedrock KB ID
        region (str): AWS region
        top_k (int): Number of retrieval results

    Returns:
        list[dict]: Retrieved structured document chunks
    """
    try:
        if not query or not query.strip():
            logger.warning("Empty query received for retrieval")
            return []

        if not knowledge_base_id:
            logger.error("Knowledge Base ID is missing")
            raise ValueError("Knowledge Base ID is required.")

        client = get_bedrock_kb_client(region)

        logger.info(f"Retrieving from KB: {knowledge_base_id} | Query: {query}")

        response = client.retrieve(
            knowledgeBaseId=knowledge_base_id,
            retrievalQuery={
                "text": query
            },
            retrievalConfiguration={
                "vectorSearchConfiguration": {
                    "numberOfResults": top_k
                }
            }
        )

        raw_results = response.get("retrievalResults", [])
        parsed_results = parse_retrieval_results(raw_results)

        logger.info(f"Retrieved {len(parsed_results)} documents from Knowledge Base")
        return parsed_results

    except (BotoCoreError, ClientError) as aws_error:
        logger.error(f"AWS Bedrock retrieval failed: {str(aws_error)}")
        raise RuntimeError("AWS Bedrock retrieval failed.") from aws_error

    except Exception as e:
        logger.error(f"Unexpected retrieval error: {str(e)}")
        raise RuntimeError("Unexpected error during knowledge base retrieval.") from e



# Optional: Retrieve Only Text Chunks

def retrieve_text_chunks(query, knowledge_base_id, region, top_k=3):
    """
    Convenience helper if only raw text chunks are needed.

    Args:
        query (str): User question
        knowledge_base_id (str): Bedrock KB ID
        region (str): AWS region
        top_k (int): Number of retrieval results

    Returns:
        list[str]: Retrieved text chunks only
    """
    docs = retrieve_from_kb(query, knowledge_base_id, region, top_k)
    return [doc["text"] for doc in docs if "text" in doc]