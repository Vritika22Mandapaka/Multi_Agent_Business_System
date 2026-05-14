import os

from dotenv import load_dotenv
from openai import OpenAIError

load_dotenv()

CHROMA_DIR = "./chroma_market"
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

_vectorstore = None


def _get_vectorstore():
    global _vectorstore

    try:
        from langchain_chroma import Chroma
        from langchain_openai import OpenAIEmbeddings
    except ModuleNotFoundError:
        return None

    if _vectorstore is None:
        _vectorstore = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=OpenAIEmbeddings(model=EMBEDDING_MODEL),
        )

    return _vectorstore


def retrieve_market_context(business_idea: str, k: int = 6) -> str:
    if not business_idea:
        return ""

    vectorstore = _get_vectorstore()

    if vectorstore is None:
        return ""

    query = f"""
    Retrieve market research context for this business idea:
    {business_idea}

    Focus on customer demand, target users, competitors, pricing, adoption barriers,
    market trends, logistics risks, and go-to-market strategy.
    """

    try:
        docs = vectorstore.similarity_search(query, k=k)
    except OpenAIError:
        return ""

    if not docs:
        return ""

    chunks = []

    for doc in docs:
        source = doc.metadata.get("source_file", "market research document")
        chunks.append(f"[Source: {source}]\n{doc.page_content}")

    return "\n\n---\n\n".join(chunks)