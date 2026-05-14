import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

CHROMA_DIR = "./chroma_regulatory"
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

_vectorstore = None


def _get_vectorstore():
    global _vectorstore

    if _vectorstore is None:
        _vectorstore = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=OpenAIEmbeddings(model=EMBEDDING_MODEL),
        )

    return _vectorstore


def retrieve_regulatory_context(business_idea: str, state: str = None, k: int = 5):
    if not business_idea:
        return ""

    try:
        vectorstore = _get_vectorstore()

        if state:
            state_docs = vectorstore.similarity_search(
                business_idea,
                k=k,
                filter={"state": state},
            )

            federal_docs = vectorstore.similarity_search(
                business_idea,
                k=2,
                filter={"state": "ALL"},
            )

            docs = state_docs + federal_docs
        else:
            docs = vectorstore.similarity_search(business_idea, k=k)

        if not docs:
            return ""

        chunks = []

        for doc in docs:
            source = doc.metadata.get("source_url", "official regulatory source")
            state_label = doc.metadata.get("state", "UNKNOWN")

            chunks.append(
                f"[State: {state_label}]\n"
                f"[Source: {source}]\n"
                f"{doc.page_content}"
            )

        return "\n\n---\n\n".join(chunks)

    except Exception as e:
        return f"Regulatory retrieval error: {str(e)}"