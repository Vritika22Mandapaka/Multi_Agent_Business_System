# AI Multi-Agent Business Decision System

This project evaluates business ideas with a multi-agent workflow. It includes separate agents for market research, technical feasibility, financial analysis, retry validation, and final synthesis.

## Stack

* LangGraph for workflow orchestration
* OpenAI for LLM calls
* LangChain OpenAI wrappers for chat and embeddings
* Streamlit for the web interface
* PyMuPDF for PDF parsing
* Chroma via `langchain-chroma` for optional regulatory RAG retrieval

## Setup

Use Python 3.12.

```powershell
py -3.12 -m venv .venv312
.\.venv312\Scripts\python.exe -m pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
LLM_BACKEND=openai
OPENAI_MODEL=gpt-5-nano
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

## Run Streamlit

```powershell
.\.venv312\Scripts\python.exe -m streamlit run streamlit_app.py
```

## Run CLI

```powershell
.\.venv312\Scripts\python.exe -m app.main
```

When prompted, enter:

```text
input/sample_business_idea.txt
```

## Optional RAG Index

To rebuild the regulatory Chroma index:

```powershell
.\.venv312\Scripts\python.exe -m rag.ingest
```

The generated `chroma_regulatory/` directory is local runtime data and should not be committed.

## Project Structure

```text
agents/          agent implementations
app/             graph, state, CLI, and LLM client
evals/           rubric and consistency checks
input/           sample input
rag/             state extraction, ingestion, and retrieval
tools/           calculator and simulated market context tools
streamlit_app.py Streamlit UI
```
