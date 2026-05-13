# rag/retrieve.py
# Pure retrieval utility — no LLM, no agent logic.
# Called from agents/synthesis_agent.py after state extraction.
#
# Place this file at: Multi_Agent_Busisys/rag/retrieve.py

import os

from openai import OpenAIError

CHROMA_DIR = "./chroma_regulatory"
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

_vectorstore = None


def _get_vectorstore():
    try:
        from langchain_chroma import Chroma
        from langchain_openai import OpenAIEmbeddings
    except ModuleNotFoundError:
        return None

    global _vectorstore
    if _vectorstore is None:
        _vectorstore = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=OpenAIEmbeddings(model=EMBEDDING_MODEL),
        )
    return _vectorstore


def retrieve_regulatory_context(business_idea: str, state: str) -> str:
    """
    Returns retrieved regulatory text for the given state.
    Matches the project's state key: 'business_idea'.

    Args:
        business_idea: from state["business_idea"]
        state: 2-letter code e.g. "NY"

    Returns:
        String of relevant regulatory chunks with source URLs.
        Returns "" if nothing found or state is None.
    """
    if not state:
        return ""

    vs = _get_vectorstore()
    if vs is None:
        return ""

    try:
        state_docs = vs.similarity_search(
            business_idea, k=5, filter={"state": state}
        )
        federal_docs = vs.similarity_search(
            business_idea, k=2, filter={"state": "ALL"}
        )
    except OpenAIError:
        return ""

    all_docs = state_docs + federal_docs
    if not all_docs:
        return ""

    chunks = []
    for doc in all_docs:
        source = doc.metadata.get("source_url", "official source")
        chunks.append(f"[Source: {source}]\n{doc.page_content}")

    return "\n\n---\n\n".join(chunks)
