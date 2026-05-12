import os
import json
import sys
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    api_key = input("Enter your OpenAI API key: ").strip()
    os.environ["OPENAI_API_KEY"] = api_key

from agents.finance_agent import finance_agent

BUSINESS_IDEA = (
    "I want to launch an AI-powered grocery delivery startup for college students "
    "that predicts weekly needs and auto-suggests smart purchases based on budget and eating habits."
)

MOCK_RESEARCH = {
    "agent": "Research Agent",
    "analysis": (
        "Market Opportunity: College students spend ~$150/month on groceries. "
        "35M+ college students in the US represent a $5B+ addressable market. "
        "Competitor Analysis: Instacart and DoorDash Grocery serve general consumers; "
        "no major player targets college students specifically. "
        "Demand Assessment: High — price sensitivity and time constraints make this segment ideal. "
        "External Risks: High churn due to graduation cycles; thin margins in grocery delivery. "
        "Confidence Score: 72"
    )
}

MOCK_TECH = {
    "agent": "Tech Stack Agent",
    "analysis": (
        "Feasibility Verdict: Feasible with moderate complexity. "
        "Recommended Tech Stack: React Native (mobile), FastAPI (backend), PostgreSQL, "
        "OpenAI API for prediction engine, Stripe for payments. "
        "Development Effort Estimate: 8–10 months for MVP with a team of 4. "
        "Technical Risks: ML model accuracy for preference prediction; "
        "third-party grocery API reliability. "
        "Confidence Score: 68"
    )
}

STATE = {
    "business_idea": BUSINESS_IDEA,
    "research_output": MOCK_RESEARCH,
    "tech_output": MOCK_TECH,
    "finance_output": None,
    "retry_output": None,
    "final_report": None,
}


def run_single():
    print("\n" + "=" * 60)
    print("  FINANCE AGENT — STANDALONE TEST")
    print("=" * 60)
    print(f"\nBusiness Idea:\n  {BUSINESS_IDEA}\n")
    print("Running finance agent...\n")

    try:
        result = finance_agent(STATE)
        output = result["finance_output"]

        print("STAGE 1 — Extracted Parameters:")
        print(json.dumps(output["extracted_parameters"], indent=2))

        print("\nSTAGE 2 — Calculator Results:")
        print(json.dumps(output["calculator_results"], indent=2))

        print("\nSTAGE 2b — Financial Health Signal:")
        print(json.dumps(output["financial_health_signal"], indent=2))

        print("\nSTAGE 3 — Financial Analysis:")
        print(json.dumps(output["analysis"], indent=2))

        print("\n" + "=" * 60)
        print(f"Confidence Score : {output['analysis'].get('confidence_score', 'N/A')} / 100")
        print(f"Confidence Range : {output['financial_health_signal']['suggested_confidence_range']}")
        print(f"Confidence Reason: {output['analysis'].get('confidence_reasoning', 'N/A')}")
        print("=" * 60)

    except ValueError as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)


def run_consistency_check(runs=3):
    print("\n" + "=" * 60)
    print(f"  CONSISTENCY CHECK — {runs} RUNS")
    print("=" * 60)

    scores = []
    risk_sets = []

    for i in range(1, runs + 1):
        print(f"\nRun {i}...", end=" ", flush=True)
        try:
            result = finance_agent(STATE)
            analysis = result["finance_output"]["analysis"]
            score = analysis.get("confidence_score", 0)
            risks = set(analysis.get("financial_risks", []))
            scores.append(score)
            risk_sets.append(risks)
            print(f"Confidence Score: {score}")
        except ValueError as e:
            print(f"FAILED: {e}")

    if len(scores) < 2:
        print("Not enough successful runs for consistency analysis.")
        return

    variance = max(scores) - min(scores)
    avg_score = round(sum(scores) / len(scores), 1)

    # Risk overlap: how many risks appear in ALL runs
    common_risks = risk_sets[0]
    for rs in risk_sets[1:]:
        common_risks = common_risks & rs

    print("\n" + "-" * 60)
    print(f"Scores       : {scores}")
    print(f"Average      : {avg_score}")
    print(f"Variance     : {variance} (low < 10 is good)")
    print(f"Consistency  : {'HIGH' if variance <= 10 else 'MODERATE' if variance <= 20 else 'LOW'}")
    print(f"Common Risks : {len(common_risks)} risk(s) appeared in all {runs} runs")
    for r in common_risks:
        print(f"  - {r[:80]}...")
    print("-" * 60)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "single"

    if mode == "consistency":
        run_consistency_check(runs=3)
    else:
        run_single()
