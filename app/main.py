import fitz

from app.graph import build_graph
from rag.extract_state import extract_state
from rag.domain_detector import detect_business_domain


def parse_input(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        try:
            return "\n".join(page.get_text() for page in doc).strip()
        finally:
            doc.close()

    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    raise ValueError("Only PDF and TXT files are supported.")


def run_multi_agent_system(business_text: str):
    app = build_graph()

    target_state = extract_state(business_text)
    business_domain = detect_business_domain(business_text)

    initial_state = {
        "business_idea": business_text,
        "business_domain": business_domain,

        "research_output": None,
        "research_eval": None,

        "tech_output": None,
        "tech_eval": None,

        "finance_output": None,

        "retry_output": None,

        "final_report": None,

        "target_state": target_state,
        "regulatory_context": None,
    }

    return app.invoke(initial_state)


def main():
    print("\nAI Multi-Agent Business Decision System\n")

    file_path = input("Enter path to your business idea file PDF or TXT: ").strip()

    try:
        business_text = parse_input(file_path)
    except Exception as e:
        print(f"Input error: {e}")
        return

    if not business_text:
        print("Input file is empty.")
        return

    target_state = extract_state(business_text)
    business_domain = detect_business_domain(business_text)

    print(f"Detected business domain: {business_domain}")

    if target_state:
        print(f"Detected state: {target_state}")
    else:
        print("No supported Northeast US state detected. Regulatory RAG will be skipped.")

    print("\nRunning multi-agent analysis...\n")

    final_state = run_multi_agent_system(business_text)

    print("\nFINAL BUSINESS DECISION REPORT")
    print("=" * 60)
    print(final_state["final_report"]["report"])

    print("\nRESEARCH EVALUATION")
    print("=" * 60)
    print(final_state.get("research_eval"))

    print("\nTECH EVALUATION")
    print("=" * 60)
    print(final_state.get("tech_eval"))

    print("\nBUSINESS DOMAIN")
    print("=" * 60)
    print(final_state.get("business_domain"))

    print("\nREGULATORY CONTEXT")
    print("=" * 60)
    if final_state.get("regulatory_context"):
        print(final_state["regulatory_context"][:2500])
    else:
        print("No regulatory context retrieved.")


if __name__ == "__main__":
    main()