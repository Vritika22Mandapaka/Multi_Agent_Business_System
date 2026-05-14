import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
MARKET_DOCS_DIR = BASE_DIR / "market_docs"
CHROMA_DIR = "./chroma_market"
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def load_market_documents():
    documents = []

    for file_path in MARKET_DOCS_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8").strip()

        if text:
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source_file": file_path.name,
                        "source_type": "market_research_doc",
                    },
                )
            )

    return documents


def split_documents(documents, chunk_size=800, overlap=100):
    chunks = []
    step = chunk_size - overlap

    for doc in documents:
        text = doc.page_content

        for start in range(0, len(text), step):
            chunk_text = text[start:start + chunk_size].strip()

            if chunk_text:
                chunks.append(
                    Document(
                        page_content=chunk_text,
                        metadata=dict(doc.metadata),
                    )
                )

    return chunks


def ingest_market_docs():
    documents = load_market_documents()

    if not documents:
        raise RuntimeError(
            "No market documents found. Make sure market_docs/*.txt exists."
        )

    chunks = split_documents(documents)

    Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(model=EMBEDDING_MODEL),
        persist_directory=CHROMA_DIR,
    )

    print(f"Ingested {len(documents)} documents.")
    print(f"Created {len(chunks)} chunks.")
    print(f"Saved market vector store to: {CHROMA_DIR}")


if __name__ == "__main__":
    ingest_market_docs()