import json
from typing import List, Dict, Any

from pydantic import BaseModel, Field

from app.llm_client import call_llm_with_system
from rag.market_retrieve import retrieve_market_context
from rag.domain_detector import detect_business_domain
from tools.web_search import get_market_context


class Competitor(BaseModel):
    name: str
    category: str
    strengths: List[str]
    weaknesses: List[str]
    differentiation_opportunity: str


class ResearchAgentOutput(BaseModel):
    market_opportunity: str
    target_customers: List[str]
    customer_pain_points: List[str]
    market_trends: List[str]
    competitor_analysis: List[Competitor]
    demand_assessment: str
    pricing_and_adoption_insights: str
    external_risks: List[str]
    go_to_market_recommendation: str
    confidence_score: int = Field(ge=0, le=100)
    confidence_reasoning: str


RESEARCH_SYSTEM_PROMPT = """
You are the Market Research Agent in a multi-agent business decision system.

Rules:
- Use the detected business domain.
- Use domain-specific RAG only when it matches the business idea.
- Do NOT force grocery, delivery, student, or campus assumptions unless the idea belongs to that domain.
- If domain-specific RAG is unavailable, perform generic business research reasoning.
- Do not invent fake statistics.
- If exact market data is unavailable, say the analysis is based on directional signals.
- Output ONLY valid JSON.
- No markdown.
- No explanation outside JSON.

Return JSON using this schema:

{
  "market_opportunity": "",
  "target_customers": [],
  "customer_pain_points": [],
  "market_trends": [],
  "competitor_analysis": [
    {
      "name": "",
      "category": "",
      "strengths": [],
      "weaknesses": [],
      "differentiation_opportunity": ""
    }
  ],
  "demand_assessment": "",
  "pricing_and_adoption_insights": "",
  "external_risks": [],
  "go_to_market_recommendation": "",
  "confidence_score": 0,
  "confidence_reasoning": ""
}
"""


def extract_json(raw_text):
    text = raw_text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found.")

    return json.loads(text[start:end + 1])


def evaluate_research_output(output: Dict[str, Any]) -> Dict[str, Any]:
    checks = {
        "market_opportunity": bool(output.get("market_opportunity")),
        "target_customers": bool(output.get("target_customers")),
        "customer_pain_points": bool(output.get("customer_pain_points")),
        "market_trends": bool(output.get("market_trends")),
        "competitor_analysis": bool(output.get("competitor_analysis")),
        "demand_assessment": bool(output.get("demand_assessment")),
        "pricing_and_adoption_insights": bool(output.get("pricing_and_adoption_insights")),
        "external_risks": bool(output.get("external_risks")),
        "go_to_market_recommendation": bool(output.get("go_to_market_recommendation")),
        "confidence_score": isinstance(output.get("confidence_score"), int),
    }

    return {
        "rubric_score": sum(1 for value in checks.values() if value),
        "max_score": len(checks),
        "checks": checks,
    }


def research_agent(state):
    business_idea = state["business_idea"]

    business_domain = (
        state.get("business_domain")
        or detect_business_domain(business_idea)
    )

    # Use Market RAG only for grocery/business-delivery style ideas
    if business_domain == "grocery":
        retrieved_market_context = retrieve_market_context(
            business_idea
        )

        rag_note = (
            "Domain-specific grocery Market RAG was used."
        )

        web_market_context = get_market_context()

    else:
        retrieved_market_context = ""

        rag_note = (
            f"Market RAG skipped because detected domain "
            f"is '{business_domain}', not grocery."
        )

        web_market_context = {
            "note": (
                "Generic business analysis mode. "
                "No grocery-specific market retrieval used."
            )
        }

    user_prompt = f"""
Business Idea:
{business_idea}

Detected Business Domain:
{business_domain}

RAG Usage Note:
{rag_note}

Retrieved Market RAG Context:
{retrieved_market_context if retrieved_market_context else "No domain-specific Market RAG context used."}

General Market Context:
{json.dumps(web_market_context, indent=2)}

Domain Instructions:

If education:
- focus on parents
- childcare demand
- licensing
- staffing
- curriculum
- tuition
- preschool/daycare competitors

If grocery:
- focus on grocery delivery
- student budgets
- recurring carts
- delivery logistics
- grocery competitors
- campus-first strategy

If healthcare:
- focus on patients
- care delivery
- compliance
- trust
- operations

If finance:
- focus on financial users
- monetization
- fintech competitors
- trust
- regulation

If general:
- provide broad business analysis
- avoid unrelated assumptions

Analyze:
1. Market opportunity
2. Target customers
3. Customer pain points
4. Market trends
5. Competitors
6. Demand assessment
7. Pricing/adoption insights
8. External risks
9. Go-to-market recommendation
10. Confidence score
"""

    raw_output = call_llm_with_system(
        RESEARCH_SYSTEM_PROMPT,
        user_prompt
    ).strip()

    try:
        parsed_output = extract_json(raw_output)

        validated_output = ResearchAgentOutput(
            **parsed_output
        )

        research_result = validated_output.model_dump()

        research_eval = evaluate_research_output(
            research_result
        )

        return {
            "business_domain": business_domain,

            "research_output": {
                "agent": "Research Agent",

                "business_domain": business_domain,

                "rag_usage_note": rag_note,

                "market_rag_context": retrieved_market_context,

                "web_market_context": web_market_context,

                "analysis": research_result,
            },

            "research_eval": research_eval,
        }

    except Exception as e:
        fallback_analysis = {
            "market_opportunity":
                "Market research analysis generated but parsing failed.",

            "target_customers": [],

            "customer_pain_points": [],

            "market_trends": [],

            "competitor_analysis": [],

            "demand_assessment":
                "Needs manual review.",

            "pricing_and_adoption_insights":
                "Needs manual review.",

            "external_risks": [
                "Research output parsing failure."
            ],

            "go_to_market_recommendation":
                "Review raw output and rerun.",

            "confidence_score": 30,

            "confidence_reasoning": str(e),

            "raw_output": raw_output,
        }

        return {
            "business_domain": business_domain,

            "research_output": {
                "agent": "Research Agent",

                "business_domain": business_domain,

                "rag_usage_note": rag_note,

                "market_rag_context": retrieved_market_context,

                "web_market_context": web_market_context,

                "analysis": fallback_analysis,
            },

            "research_eval": evaluate_research_output(
                fallback_analysis
            ),
        }