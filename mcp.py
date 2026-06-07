# backend/mcp.py

from datetime import datetime
from typing import List, Dict

def generate_mcp(
    request_id: str,
    user_id: str,
    query: str,
    doc_ids: List[str],
    retriever: str = "chroma",
    model_version: str = "gpt-4",
    prompt_id: str = "default-prompt-v1",
    conversation_id: str = "conv-001"
) -> Dict:
    """
    Generates a structured metadata (MCP) payload for logging or Kafka.
    """
    mcp = {
        "request_id": request_id,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "query": query,
        "conversation_id": conversation_id,
        "metadata": {
            "retriever": retriever,
            "model_version": model_version,
            "prompt_id": prompt_id,
            "doc_ids": doc_ids
        }
    }
    return mcp
