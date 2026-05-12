import fitz

from app.graph import build_graph
from rag.extract_state import extract_state


def parse_input(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        try:
            return "\n".join(page.get_text() for page in doc).strip()
        finally:
            doc.close()

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def main():
    file_path = input("Enter path to your business idea file (PDF or TXT): ").strip()
    business_idea = parse_input(file_path)

    target_state = extract_state(business_idea)
    if target_state:
        print(f"Detected state: {target_state}")
    else:
        print("No Northeast US state detected. Regulatory compliance will be skipped.")

    app = build_graph()

    initial_state = {
        "business_idea": business_idea,
        "research_output": None,
        "tech_output": None,
        "finance_output": None,
        "retry_output": None,
        "final_report": None,
        "target_state": target_state,
        "regulatory_context": None,
    }

    final_state = app.invoke(initial_state)
    print("\n" + "=" * 60)
    print(final_state["final_report"]["report"])


if __name__ == "__main__":
    main()
