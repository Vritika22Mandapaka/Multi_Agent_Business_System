# AI Multi-Agent Business Decision System

## Project Overview

This project is an AI-powered **Multi-Agent Business Decision System** built for **FE524 – Prompt Engineering Lab for Business Applications** at **Stevens Institute of Technology**.

The system evaluates business ideas by simulating how real companies make strategic decisions. Instead of relying on separate teams for market research, technical feasibility, financial analysis, and compliance review, this project uses multiple AI agents inside a single LangGraph workflow to generate one final business recommendation.

The final output includes:

- Go / No-Go decision
- Overall confidence score
- Market analysis
- Technical feasibility report
- Financial viability report
- Regulatory compliance context
- Consolidated risk list
- Final recommendation
- Downloadable Word report from the Streamlit interface

---

## Business Problem

When companies evaluate a new product, startup idea, or market-entry strategy, they usually need multiple teams working separately:

- Market research team
- Technology team
- Finance team
- Compliance or regulatory team
- Strategy team

This creates common business problems:

- Slow decision-making
- Inconsistent assumptions across teams
- Fragmented recommendations
- Delayed execution
- Difficulty comparing feasibility across market, technology, and finance

This project solves the problem by using AI agents that work together in a coordinated workflow. Each agent specializes in one decision area, and the synthesis layer combines the outputs into a single final report.

---

## System Architecture

The system is built using:

- **LangGraph** for multi-agent workflow orchestration
- **LangChain** for model wrappers and embedding integrations
- **OpenAI GPT-5 nano** as the primary LLM
- **OpenAI Embeddings** for vector search
- **ChromaDB** for local vector storage
- **PyMuPDF** for PDF parsing
- **Python tools** for calculator and market context utilities
- **Streamlit** for the interactive web interface
- **python-docx** for downloadable Word reports
- **llama.cpp fallback-ready structure** for optional local LLM support

---

## High-Level Workflow

```text
Business Idea Input
        ↓
PDF/TXT Parsing or Manual Input
        ↓
Domain Detection
        ↓
Research Agent
(Market RAG + Market Context Tool when domain matches)
        ↓
Technology Agent
(System Architecture + Implementation Plan)
        ↓
Finance Agent
(Calculator Tool + Unit Economics)
        ↓
Regulatory RAG
(State-Specific Compliance Retrieval)
        ↓
Synthesis Agent
(Final Business Decision Report)
        ↓
Evaluation Layer
(Rubric + Consistency Check)
        ↓
Downloadable Word Report
```

---

## Agent Workflow

### Agent 1 — Research Agent

The Research Agent evaluates the business idea from a market and customer perspective.

Responsibilities:

- Market opportunity analysis
- Target customer identification
- Customer pain-point analysis
- Market trend analysis
- Competitor analysis
- Demand assessment
- Pricing and adoption insights
- External risk identification
- Go-to-market recommendation
- Confidence score generation

Tools and retrieval:

- Market RAG for domain-specific grocery/startup context
- Market context tool
- Domain-aware fallback for non-grocery ideas

Output:

- Structured JSON research analysis
- Market opportunity summary
- Competitor analysis
- Demand assessment
- Risk flags
- Confidence score

---

### Agent 2 — Technology Agent

The Technology Agent evaluates whether the business idea is technically feasible.

Responsibilities:

- Technical feasibility assessment
- Recommended technology stack
- System architecture design
- Frontend and backend requirements
- Database and cloud infrastructure recommendations
- AI/ML architecture planning
- Deployment and monitoring plan
- Technical risk analysis
- Development timeline and MVP planning

Output includes:

- Feasibility verdict
- Project requirements
- Systems architecture
- Development effort
- Operational requirements
- Technical risks
- Confidence score

---

### Agent 3 — Finance Agent

The Finance Agent evaluates financial feasibility using extracted parameters and calculator-based analysis.

Responsibilities:

- Startup cost estimation
- Revenue model analysis
- Variable and fixed cost estimation
- Contribution margin calculation
- Break-even calculation
- ROI projection
- Payback period calculation
- Financial risk analysis
- Confidence score generation

Tool used:

- Calculator Tool

Output includes:

- Startup costs
- Monthly operating costs
- Revenue model
- ROI projection
- Break-even analysis
- Payback period
- Financial risks
- Confidence score

---

### Retry Agent

The Retry Agent is designed to improve reliability when outputs are uncertain or confidence is low.

Used when:

- Confidence score is too low
- High-risk signals are detected
- Business feasibility is uncertain
- Finance or technology outputs indicate major concerns

Purpose:

- Re-analyze weak areas
- Improve decision reliability
- Add a second-pass review pattern similar to real business decision workflows

---

### Synthesis Agent

The Synthesis Agent combines outputs from all agents into a final decision report.

Responsibilities:

- Combine research, technology, finance, and regulatory outputs
- Generate a final Go / No-Go recommendation
- Assign an overall confidence score
- Summarize opportunities and risks
- Include regulatory context when available
- Provide practical next steps

Final output includes:

- Final verdict
- Overall confidence score
- Research summary
- Technology summary
- Finance summary
- Regulatory compliance summary
- Consolidated risk list
- Final recommendation

---

## Retrieval-Augmented Generation (RAG)

This project includes two RAG pipelines.

### 1. Market RAG

Market RAG supports the Research Agent when the detected domain matches the available market documents.

Current Market RAG documents include:

- Grocery delivery market context
- Student spending behavior
- AI personalization in retail
- Delivery logistics risks

Market RAG workflow:

```text
market_docs/
        ↓
Text Chunking
        ↓
OpenAI Embeddings
        ↓
ChromaDB Vector Store
        ↓
Similarity Search
        ↓
Research Agent Context Injection
```

Market RAG helps the system provide grounded insights about:

- Customer demand
- Competitors
- Student pricing sensitivity
- Delivery logistics risks
- AI personalization opportunities
- Campus-first launch strategy

---

### 2. Regulatory RAG

Regulatory RAG supports the Synthesis Agent by retrieving state-specific compliance context.

Supported states:

- New Jersey (NJ)
- New York (NY)
- Pennsylvania (PA)
- Connecticut (CT)
- Massachusetts (MA)

Regulatory RAG retrieves context from official business registration and government sources.

Examples of retrieved information:

- NJ-REG business registration requirement
- State business formation guidance
- Tax registration guidance
- SBA business registration guidance

Regulatory RAG workflow:

```text
Official Regulatory Sources
        ↓
Document Loading
        ↓
Text Chunking
        ↓
OpenAI Embeddings
        ↓
ChromaDB Vector Store
        ↓
State-Aware Retrieval
        ↓
Synthesis Agent Compliance Summary
```

---

## Domain-Aware Routing

A domain detection layer was added to prevent unrelated RAG retrieval and reduce hallucinations.

Supported detected domains:

- Grocery
- Education
- Healthcare
- Finance
- General business

Example behavior:

```text
Input: AI grocery delivery startup in New Jersey
Detected Domain: grocery
Action: Uses Market RAG + Regulatory RAG

Input: I want to start a preschool program
Detected Domain: education
Action: Skips grocery Market RAG and performs generic education-focused business analysis

Input: Enterprise safety platform in New Jersey
Detected Domain: general
Action: Uses generic business analysis and state regulatory retrieval if NJ is detected
```

This improves answer validity by preventing grocery-specific context from leaking into unrelated domains.

---

## Features Implemented

### Core Features

- PDF input support
- TXT input support
- Manual text input support
- GPT-5 nano integration
- OpenAI API integration
- Local LLM fallback-ready structure
- LangGraph multi-agent execution
- Shared typed state across agents
- Final synthesis generation

### Tool Usage

- Market context tool for Research Agent
- Calculator Tool for Finance Agent
- State extraction tool for Regulatory RAG
- Domain detection tool for domain-aware routing

### RAG Features

- Market RAG using ChromaDB
- Regulatory RAG using ChromaDB
- OpenAI embedding-based retrieval
- Domain-specific retrieval control
- State-aware regulatory retrieval
- Retrieved context preview in Streamlit

### Evaluation Features

- Rubric-based scoring
- Research Agent scoring
- Technology Agent scoring
- Finance Agent scoring
- Synthesis scoring
- Consistency check across multiple runs
- Confidence validation
- Structured output evaluation

### Streamlit UI Features

- Professional dashboard interface
- PDF/TXT upload
- Manual business idea input
- Domain detection display
- State detection display
- Executive summary cards
- Final report rendering
- Agent-level output tabs
- Research RAG context viewer
- Regulatory context viewer
- Rubric evaluation display
- Consistency check button
- Download final report as Word document

---

## Project Structure

```text
Multi_Agent_Busisys/
│
├── agents/
│   ├── research_agent.py
│   ├── tech_agent.py
│   ├── finance_agent.py
│   ├── retry_agent.py
│   ├── synthesis_agent.py
│   └── __init__.py
│
├── app/
│   ├── main.py
│   ├── graph.py
│   ├── state.py
│   ├── llm_client.py
│   └── __init__.py
│
├── evals/
│   ├── rubric_eval.py
│   ├── consistency_check.py
│   └── __init__.py
│
├── rag/
│   ├── domain_detector.py
│   ├── extract_state.py
│   ├── ingest.py
│   ├── retrieve.py
│   ├── market_ingest.py
│   ├── market_retrieve.py
│   └── __init__.py
│
├── tools/
│   ├── calculator.py
│   ├── web_search.py
│   └── __init__.py
│
├── market_docs/
│   ├── grocery_delivery_market.txt
│   ├── student_spending_behavior.txt
│   ├── ai_personalization_retail.txt
│   └── delivery_logistics_risks.txt
│
├── input/
│   └── sample_business_idea.txt
│
├── output/
│
├── chroma_market/
├── chroma_regulatory/
│
├── streamlit_app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

Note: `chroma_market/` and `chroma_regulatory/` are generated local vector database folders. They may be excluded from GitHub if the project rebuilds them using ingestion scripts.

---

## Installation

### Step 1 — Create Virtual Environment

```powershell
py -m venv venv
```

Activate it:

```powershell
.\\venv\\Scripts\\activate
```

Alternative Python 3.12 setup:

```powershell
py -3.12 -m venv .venv312
.\\.venv312\\Scripts\\activate
```

---

### Step 2 — Install Requirements

```powershell
pip install -r requirements.txt
```

If needed, install additional packages:

```powershell
pip install langchain-chroma python-docx
```

---

### Step 3 — Add Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
LLM_BACKEND=openai
OPENAI_MODEL=gpt-5-nano
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

---

## Build Vector Stores

### Market RAG Ingestion

Run:

```powershell
py -m rag.market_ingest
```

Expected output:

```text
Ingested 4 documents.
Created XX chunks.
Saved market vector store to: ./chroma_market
```

---

### Regulatory RAG Ingestion

Run:

```powershell
py -m rag.ingest
```

Expected output:

```text
Indexing regulatory chunks into ChromaDB...
Vectorstore saved to ./chroma_regulatory
```

Some government pages may return 403 errors. This is acceptable if other official sources load successfully.

---

## Running the Project

### Terminal Version

```powershell
py -m app.main
```

When prompted, enter:

```text
input/sample_business_idea.txt
```

or any custom PDF/TXT business idea file path.

---

### Streamlit Web App Version

```powershell
streamlit run streamlit_app.py
```

The Streamlit app allows users to:

- Upload PDF/TXT files
- Type business ideas manually
- Run complete multi-agent analysis
- View final reports
- Inspect all agent outputs
- See RAG context
- Check rubric scores
- Run consistency checks
- Download the final report as a Word document

---

## Example Inputs

### Grocery Startup Example

```text
I want to launch an AI-powered grocery delivery startup in New Jersey for college students that predicts weekly needs and auto-suggests smart purchases based on budget and eating habits.
```

Expected behavior:

- Detected Domain: grocery
- Detected State: NJ
- Market RAG used
- Regulatory RAG retrieved
- Final report includes NJ registration guidance

---

### Preschool Program Example

```text
I want to start a preschool program in New Jersey.
```

Expected behavior:

- Detected Domain: education
- Grocery Market RAG skipped
- Regulatory RAG retrieved if state is detected
- Output focuses on childcare, parents, staffing, tuition, curriculum, and licensing concerns

---

### Enterprise Safety Platform Example

```text
I want to build an enterprise safety and incident management platform for companies in New Jersey.
```

Expected behavior:

- Detected Domain: general
- Generic business reasoning
- Regulatory RAG retrieved if state is detected
- Output focuses on enterprise safety, compliance, security, operations, and risk management

---

## Evaluation Metrics

### Rubric-Based Scoring

Each agent is scored based on required outputs.

Examples:

- Research Agent → market, competitors, demand, risk
- Technology Agent → architecture, backend, timeline, risk
- Finance Agent → cost, ROI, break-even, payback
- Synthesis Layer → verdict, confidence, recommendation, risk

---

### Consistency Check

The system can run the same input multiple times and compare final outputs.

It evaluates:

- Recommendation stability
- Confidence score consistency
- Repeated conclusion alignment
- Overall report consistency

Example:

```text
Consistency Score: 87.5%
```

---

## Example Final Output

```text
Final Verdict:
Proceed with a campus-first MVP pilot in New Jersey.

Overall Confidence Score:
68/100

Research Summary:
Strong student-focused opportunity with budget-aware grocery planning.

Technology Summary:
Feasible using microservices, recommendation systems, API gateway, and cloud deployment.

Finance Summary:
Requires careful validation of delivery costs, ROI, break-even volume, and payback period.

Regulatory Summary:
NJ-REG business registration should be completed before operating in New Jersey.

Final Recommendation:
Launch a lean pilot, measure retention and unit economics, then scale if validated.
```

---

## Course Concepts Used

| Course Topic | Implementation |
| --- | --- |
| Prompt Engineering | Agent prompt design and structured instructions |
| Zero-shot Prompting | General business idea analysis |
| Few-shot Style Guidance | Agent-specific formatting and schema control |
| Tool Use | Calculator Tool and Market Context Tool |
| Retrieval-Augmented Generation | Market RAG and Regulatory RAG |
| Embeddings | OpenAI embeddings for vector retrieval |
| Vector Database | ChromaDB for local retrieval |
| Multi-Agent Systems | Research, Tech, Finance, Retry, and Synthesis Agents |
| LangGraph | Workflow orchestration and state passing |
| Evaluation | Rubric scoring and consistency checks |
| Structured Outputs | JSON outputs from agents |
| UI Development | Streamlit interactive dashboard |
| Document Generation | Downloadable Word report |

---

## Strengths of the System

- Uses specialized agents instead of one generic prompt
- Combines LLM reasoning with tools and retrieval
- Supports domain-aware routing to reduce hallucinations
- Retrieves official regulatory context when state is detected
- Produces structured and explainable outputs
- Provides evaluation metrics for agent performance
- Includes a professional Streamlit demo interface
- Generates downloadable reports for business review

---

## Known Limitations

- Market RAG is currently strongest for grocery/student-delivery business ideas
- Regulatory RAG focuses mainly on business registration and state compliance sources
- Some regulatory pages may block scraping or return 403 errors
- Financial projections are estimated and should be validated with real business data
- Domain detection is keyword-based and can be expanded with a classifier
- Non-supported states will skip regulatory retrieval
- Domain-specific RAG datasets need to be added for more industries

---

## Future Enhancements

- Add domain-specific RAG for education, healthcare, fintech, and security
- Add real-time web search APIs
- Add live market-size estimation
- Add more robust domain classifier
- Add deeper regulatory retrieval for childcare, healthcare, and food-delivery licenses
- Add investor pitch deck generation
- Add automated Excel financial model generation
- Deploy Streamlit app to cloud
- Add authentication and saved report history
- Add comparison mode for multiple business ideas

---

## Authors

- Sri Harsha Chinta
- Kamakshi Padma Vritika Manadapaka
- Siddharth Raju Vysyaraju
- Sri Lasya Siripurapu

---

## Final Note

This project demonstrates how modern AI agents can support real-world business strategy decisions using structured reasoning, tool calling, retrieval-augmented generation, domain-aware routing, evaluation systems, and an interactive presentation layer.

It is designed to reflect realistic enterprise decision-making workflows rather than simple single-prompt LLM outputs.
