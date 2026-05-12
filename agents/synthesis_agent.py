<<<<<<< HEAD
from app.llm_client import get_llm_client
from rag.retrieve import retrieve_regulatory_context


SYNTHESIS_PROMPT = """You are the final synthesis layer of an AI business decision system.

Business Idea:
{business_idea}

Research Agent Output:
{research_output}

Technology Agent Output:
{tech_output}

Finance Agent Output:
{finance_output}

{retry_section}

Produce the final business decision report with these sections:

### 1. Go / No-Go Verdict
State your verdict clearly with a confidence score from 0-100.

### 2. Summary per Agent
Short paragraph for each of: Market Research, Technology, Finance.

### 3. Consolidated Risk List
Deduplicate and rank all risks from across agents.

### 4. Regulatory Compliance - {state_label}
Write a structured compliance section, not a table.

Use the retrieved government source excerpts as the primary evidence. You may also include reasonable, clearly-labeled practical implications that are directly related to the business idea and the retrieved context. Do not invent exact fees, forms, deadlines, or agency requirements unless they appear in the retrieved context.

If the retrieved context is missing or thin, say that the available retrieved context was insufficient, then provide a cautious checklist of what the founder should verify with official state, local, or federal sources.

Retrieved regulatory context:
{regulatory_context}

Use this structure:

**Compliance Overview**
Briefly explain the likely regulatory posture for this business in {state_label}.

**Relevant Retrieved Context**
Summarize the most relevant points found in the retrieved context. Include source names or URLs when available.

**Likely Compliance Steps**
List practical steps the founder should take, such as business registration, tax setup, licenses or permits to verify, privacy or consumer-protection considerations, and any industry-specific checks suggested by the business idea.

**Open Questions To Verify**
List gaps that still require confirmation from official state, local, or federal sources.

### 5. Final Recommendation
Three concrete next steps the founder should take this month.
"""


NO_STATE_PROMPT = """You are the final synthesis layer of an AI business decision system.

Business Idea:
{business_idea}

Research Agent Output:
{research_output}

Technology Agent Output:
{tech_output}

Finance Agent Output:
{finance_output}

{retry_section}

Produce the final business decision report with these sections:

### 1. Go / No-Go Verdict
State your verdict clearly with a confidence score from 0-100.

### 2. Summary per Agent
Short paragraph for each of: Market Research, Technology, Finance.

### 3. Consolidated Risk List
Deduplicate and rank all risks from across agents.

### 4. Final Recommendation
Three concrete next steps the founder should take this month.
"""


def run_synthesis_agent(state: dict) -> dict:
    llm = get_llm_client()

    business_idea = state["business_idea"]
    research_output = state["research_output"]["analysis"] if state.get("research_output") else "Not available"
    tech_output = state["tech_output"]["analysis"] if state.get("tech_output") else "Not available"
    finance_output = state["finance_output"]["analysis"] if state.get("finance_output") else "Not available"

    retry_section = ""
    if state.get("retry_output"):
        retry_section = f"Retry Agent Output:\n{state['retry_output']['analysis']}"

    target_state = state.get("target_state")
    regulatory_context = None

    if target_state:
        regulatory_context = retrieve_regulatory_context(business_idea, target_state)
        prompt = SYNTHESIS_PROMPT.format(
            business_idea=business_idea,
            research_output=research_output,
            tech_output=tech_output,
            finance_output=finance_output,
            retry_section=retry_section,
            state_label=target_state,
            regulatory_context=regulatory_context or "No regulatory data retrieved.",
        )
    else:
        prompt = NO_STATE_PROMPT.format(
            business_idea=business_idea,
            research_output=research_output,
            tech_output=tech_output,
            finance_output=finance_output,
            retry_section=retry_section,
        )

    response = llm.invoke(prompt)
    report = response.content.strip()

    return {
        **state,
        "final_report": {"report": report},
        "regulatory_context": regulatory_context,
    }


synthesis_agent = run_synthesis_agent
=======
from app.llm_client import call_llm


def synthesis_agent(state):
    business_idea = state["business_idea"]

    research_output = state.get("research_output", {})
    tech_output = state.get("tech_output", {})
    finance_output = state.get("finance_output", {})
    retry_output = state.get("retry_output", {})

    prompt = f"""
You are the Synthesis Layer.

Combine all agent outputs into one final business decision report.

Business Idea:
{business_idea}

Research Output:
{research_output}

Tech Output:
{tech_output}

Finance Output:
{finance_output}

Retry Output:
{retry_output}

Return the answer in this exact structure:

Final Verdict:
Overall Confidence Score:
Research Summary:
Technology Summary:
Finance Summary:
Consolidated Risk List:
Final Recommendation:
"""

    result = call_llm(prompt)

    return {
        "final_report": {
            "agent": "Synthesis Agent",
            "report": result
        }
    }
>>>>>>> 0cf9a73e5092f5ac90c892b8da090b6bdabebf33
