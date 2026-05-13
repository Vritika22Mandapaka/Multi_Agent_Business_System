import os
import re
from html.parser import HTMLParser

import requests
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

load_dotenv()

SOURCES = [
    {"state": "NY", "url": "https://dos.ny.gov/form-corporation-or-business"},
    {"state": "NY", "url": "https://dos.ny.gov/forming-limited-liability-company-new-york"},
    {"state": "NY", "url": "https://www.ny.gov/services/start-business-new-York-state"},
    {"state": "NJ", "url": "https://business.nj.gov/pages/register-your-business"},
    {"state": "NJ", "url": "https://www.nj.gov/treasury/revenue/gettingregistered.shtml"},
    {"state": "NJ", "url": "https://www.nj.gov/treasury/taxation/br1.shtml"},
    {"state": "PA", "url": "https://business.pa.gov/register/"},
    {"state": "PA", "url": "https://www.pa.gov/services/dos/register-a-business"},
    {"state": "CT", "url": "https://business.ct.gov/"},
    {"state": "MA", "url": "https://www.mass.gov/info-details/starting-a-business-in-massachusetts"},
    {"state": "MA", "url": "https://www.mass.gov/info-details/start-build-your-business"},
    {"state": "ALL", "url": "https://www.sba.gov/business-guide/launch-your-business/register-your-business"},
]

CHROMA_DIR = "./chroma_regulatory"
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._ignored_depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self._ignored_depth += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"} and self._ignored_depth:
            self._ignored_depth -= 1

    def handle_data(self, data):
        if self._ignored_depth:
            return

        text = data.strip()
        if text:
            self.parts.append(text)

    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.parts)).strip()


def load_web_document(item: dict) -> Document:
    response = requests.get(item["url"], timeout=20)
    response.raise_for_status()

    parser = TextExtractor()
    parser.feed(response.text)

    return Document(
        page_content=parser.text(),
        metadata={"state": item["state"], "source_url": item["url"]},
    )


def split_documents(
    docs: list[Document],
    chunk_size: int = 800,
    overlap: int = 100,
) -> list[Document]:
    chunks = []
    step = chunk_size - overlap

    for doc in docs:
        for start in range(0, len(doc.page_content), step):
            chunk = doc.page_content[start : start + chunk_size].strip()
            if chunk:
                chunks.append(Document(page_content=chunk, metadata=dict(doc.metadata)))

    return chunks


def ingest():
    all_docs = []

    for item in SOURCES:
        print(f"Loading [{item['state']}] {item['url']}")
        try:
            all_docs.append(load_web_document(item))
            print("  Loaded 1 page")
        except Exception as e:
            print(f"  Failed: {e}")

    if not all_docs:
        raise RuntimeError("No documents loaded. Check your internet connection.")

    chunks = split_documents(all_docs)

    print(f"\nIndexing {len(chunks)} chunks into ChromaDB...")
    Chroma.from_documents(
        chunks,
        OpenAIEmbeddings(model=EMBEDDING_MODEL),
        persist_directory=CHROMA_DIR,
    )
    print(f"Vectorstore saved to {CHROMA_DIR}")


if __name__ == "__main__":
    ingest()
