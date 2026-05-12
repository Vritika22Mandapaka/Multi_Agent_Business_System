# AI Multi-Agent Business Decision System

## Project Overview

This project is an AI-powered multi-agent business decision system for evaluating startup or product ideas.

The system simulates a strategy review by running separate agents for:

* Market research
* Technical feasibility
* Financial analysis
* Retry validation when confidence is low
* Final synthesis and recommendation

The project includes both a command-line entry point and a Streamlit web interface.

## System Architecture

The system uses:

* LangGraph for multi-agent workflow orchestration
* LangChain OpenAI wrappers for chat model calls
* OpenAI as the primary LLM backend
* PyMuPDF for PDF parsing
* Streamlit for the demo UI
* Chroma via `langchain-chroma` for optional regulatory RAG retrieval

## Agent Workflow

1. Research Agent
   Analyzes market trends, competitors, demand, and external risks.

2. Technology Stack Agent
   Evaluates technical feasibility, stack choices, development effort, and technical risks.

3. Finance Agent
   Uses calculator outputs to estimate startup costs, ROI, break-even, payback period, and financial risks.

4. Retry Agent
   Re-evaluates the idea if low-confidence or high-risk signals are detected.

5. Synthesis Agent
   Combines all outputs into one final decision report. If a supported Northeast US state is detected, it adds a structured regulatory compliance section using retrieved RAG context when available.

Supported state detection currently focuses on:

* NY
* NJ
* PA
* CT
* MA

## Project Structure

```text
Multi_Agent_Business_System/
  agents/
    research_agent.py
    tech_agent.py
    finance_agent.py
    retry_agent.py
    synthesis_agent.py
  app/
    graph.py
    llm_client.py
    main.py
    state.py
  evals/
    consistency_check.py
    rubric_eval.py
  input/
    sample_business_idea.txt
  rag/
    extract_state.py
    ingest.py
    retrieve.py
  tools/
    calculator.py
    web_search.py
  requirements.txt
  streamlit_app.py
```

## Setup

Use Python 3.12 for this project. Some dependencies do not install cleanly on Python 3.14.

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

## Git Notes

Do not commit:

* `.env`
* `.venv/`
* `.venv312/`
* `chroma_regulatory/`
* `__pycache__/`

Commit source files, requirements, README, sample input, and RAG code.
