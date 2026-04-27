# AI Multi-Agent Business Decision System

## Project Overview

This project is an AI-powered Multi-Agent Business Decision System built for **FE524 – Prompt Engineering Lab for Business Applications** at **Stevens Institute of Technology**.

The system helps evaluate a business idea by simulating how real companies make strategic decisions.

Instead of relying on separate teams for:

* Market Research
* Technical Feasibility
* Financial Analysis

this system uses multiple AI agents to perform all three analyses automatically and generates one final business recommendation.

The final output includes:

* Go / No-Go decision
* Confidence Score
* Market analysis
* Technical feasibility report
* Financial viability report
* Consolidated risk list
* Final recommendation

---

## Business Problem

When companies plan major strategic decisions such as:

* launching a new product
* entering a new market
* building a startup

they usually need multiple teams working separately.

This creates problems like:

* slow decision-making
* inconsistent assumptions
* delayed execution
* fragmented recommendations

This project solves that by using AI agents working together inside a single LangGraph workflow.

---

## System Architecture

The system is built using:

* **LangGraph** → multi-agent workflow orchestration
* **LangChain** → prompt templates and model wrappers
* **OpenAI GPT-5 nano** → primary LLM
* **llama.cpp (fallback-ready)** → local LLM backup
* **PyMuPDF** → PDF input parsing
* **Python tools** → calculator + web search simulation

---

## Agent Workflow

## Agent 1 — Research Agent

Responsible for:

* Market trends
* Competitor analysis
* Demand estimation
* External risks

Tool used:

* Web Search Tool

Output:

* Market opportunity summary
* Competitor analysis
* Demand assessment
* External risk flags

---

## Agent 2 — Technology Stack Agent

Responsible for:

* Technical feasibility
* Stack recommendation
* Development effort estimate
* Technical risks

Output:

* Feasibility verdict
* Recommended tech stack
* Development effort
* Technical risks

---

## Agent 3 — Finance Agent

Responsible for:

* Startup cost estimation
* ROI analysis
* Break-even calculation
* Payback period
* Financial risks

Tool used:

* Calculator Tool

Output:

* Cost breakdown
* ROI projection
* Break-even analysis
* Financial risk flags

---

## Retry Agent

Responsible for:

* Re-analysis when confidence is low

Used when:

* confidence score is too low
* high-risk signals are detected
* business feasibility is uncertain

This improves reliability and matches real multi-agent decision systems.

---

## Synthesis Layer

Responsible for:

* Combining all agent outputs

Final output:

* Final Verdict
* Overall Confidence Score
* Research Summary
* Technology Summary
* Finance Summary
* Consolidated Risk List
* Final Recommendation

---

## Features Implemented

### Core Features

* PDF input support
* TXT input support
* GPT-5 nano integration
* OpenAI API connection
* Local LLM fallback-ready structure
* LangGraph multi-agent execution

### Tool Usage

* Web Search Tool for Research Agent
* Calculator Tool for Finance Agent

### Advanced Features

* Parallel/branching workflow
* Conditional retry routing
* Low-confidence retry node
* Shared typed state
* Final synthesis node

### Evaluation Features

* Rubric-based scoring
* Consistency check across multiple runs
* Confidence validation
* Structured output evaluation

---

## Project Structure

```text
Multi_Agent_Busisys/
│
├── app/
│   ├── main.py
│   ├── graph.py
│   ├── state.py
│   ├── llm_client.py
│   └── __init__.py
│
├── agents/
│   ├── research_agent.py
│   ├── tech_agent.py
│   ├── finance_agent.py
│   ├── retry_agent.py
│   ├── synthesis_agent.py
│   └── __init__.py
│
├── tools/
│   ├── calculator.py
│   ├── web_search.py
│   └── __init__.py
│
├── evals/
│   ├── rubric_eval.py
│   ├── consistency_check.py
│   └── __init__.py
│
├── input/
│   └── sample_business_idea.txt
│
├── output/
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Installation

### Step 1 — Create Virtual Environment

```powershell
py -m venv .venv
.\.venv\Scripts\activate
```

---

### Step 2 — Install Requirements

```powershell
pip install -r requirements.txt
```

---

### Step 3 — Add Environment Variables

Create `.env`

```env
OPENAI_API_KEY=your_api_key_here
LLM_BACKEND=openai
OPENAI_MODEL=gpt-5-nano
```

---

## Running the Project

Run:

```powershell
py -m app.main
```

Then enter:

```text
input/sample_business_idea.txt
```

or any custom PDF/TXT business idea file.

---

## Evaluation Metrics

## Rubric-Based Scoring

Each agent is scored based on required outputs.

Example:

* Research Agent → market, competitors, demand, risk
* Finance Agent → cost, ROI, break-even, payback

---

## Consistency Check

The same input is run multiple times.

The system compares:

* recommendation quality
* confidence stability
* repeated conclusions

This validates output consistency.

Example result:

```text
Consistency Score: 87.5%
```

---

## Example Final Output

```text
Final Verdict:
Proceed with campus-first MVP

Confidence Score:
7.5 / 10

Break-even:
55,437 orders/month

ROI:
523%

Payback Period:
18.1 months
```

---

## Course Concepts Used

| Course Topic       | Implementation             |
| ------------------ | -------------------------- |
| Few-shot prompting | Agent prompt design        |
| Chain-of-thought   | Synthesis reasoning        |
| Tool use           | Calculator + Web Search    |
| Open models        | llama.cpp fallback         |
| LangGraph          | Multi-agent orchestration  |
| Evaluation         | Rubric + Consistency       |
| Prompt Engineering | Zero-shot + Few-shot + CoT |

---

## Authors

* Sri Harsha Chinta
* Kamakshi Padma Vritika Manadapaka
* Siddharth Raju Vysyaraju
* Sri Lasya Siripurapu

---

## Final Note

This project demonstrates how modern AI agents can support real-world business strategy decisions using:

* structured reasoning
* tool calling
* evaluation systems
* multi-agent orchestration

rather than simple single-prompt LLM outputs.

It is designed to reflect realistic enterprise decision-making workflows.
