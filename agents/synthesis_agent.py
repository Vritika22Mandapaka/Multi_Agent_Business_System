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
Write a detailed summary for each agent below (3-5 sentences each). Cover key findings, specific outputs, and how they affect the overall decision.

**Market Research Agent**
Summarize market opportunity, competitor landscape, demand signals, and external risks identified.

**Technology Agent**
Summarize the recommended tech stack (frontend, backend, database, AI/ML), architecture style, MVP and full platform timeline, team size and key roles, and the top compliance or reliability concerns.

**Finance Agent**
Summarize startup costs, monthly burn, revenue model, year-1 ROI, break-even demand, payback period, and what the numbers mean for investor risk.

### 3. Consolidated Risk List
Deduplicate and rank all risks from across agents. For each risk, briefly explain the impact.

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
Three concrete, actionable next steps the founder should take this month. For each step, specify what to do, why it matters, and a target outcome.
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
Write a detailed summary for each agent below (3-5 sentences each). Cover key findings, specific outputs, and how they affect the overall decision.

**Market Research Agent**
Summarize market opportunity, competitor landscape, demand signals, and external risks identified.

**Technology Agent**
Summarize the recommended tech stack (frontend, backend, database, AI/ML), architecture style, MVP and full platform timeline, team size and key roles, and the top compliance or reliability concerns.

**Finance Agent**
Summarize startup costs, monthly burn, revenue model, year-1 ROI, break-even demand, payback period, and what the numbers mean for investor risk.

### 3. Consolidated Risk List
Deduplicate and rank all risks from across agents. For each risk, briefly explain the impact.

### 4. Final Recommendation
Three concrete, actionable next steps the founder should take this month. For each step, specify what to do, why it matters, and a target outcome.
"""


def synthesis_agent(state: dict) -> dict:
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
