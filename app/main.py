import os
import fitz
from dotenv import load_dotenv
from evals.rubric_eval import run_rubric_evaluation
from app.graph import build_graph
from evals.consistency_check import run_consistency_check


load_dotenv()


def extract_text_from_pdf(pdf_path):
    text = ""

    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text()

    doc.close()

    return text.strip()


def load_business_input():
    file_path = input("Enter PDF or TXT file path: ").strip()

    if not os.path.exists(file_path):
        print("File not found.")
        return None

    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    print("Only PDF and TXT files are supported.")
    return None


def run_multi_agent_system(business_text):
    app = build_graph()

    initial_state = {
        "business_idea": business_text,
        "research_output": None,
        "tech_output": None,
        "finance_output": None,
        "retry_output": None,
        "final_report": None
    }

    final_state = app.invoke(initial_state)

    return final_state


if __name__ == "__main__":
    print("\n   AI Multi-Agent Business Decision System \n")

    business_text = load_business_input()

    if business_text:
        print("\nInput Loaded Successfully")
        print("\nRunning Multi-Agent Analysis...\n")

        final_state = run_multi_agent_system(business_text)

        print("\n  FINAL BUSINESS DECISION REPORT \n")
        print(final_state["final_report"]["report"])

        print("\n   RUBRIC-BASED EVALUATION \n")

        evaluation_results = run_rubric_evaluation(final_state)

        for agent, result in evaluation_results.items():
         print(f"{agent}")
         print(f"Score: {result['score']} / {result['total']}")

        if result["missing"]:
         print("Missing:", ", ".join(result["missing"]))

        print("-" * 10)

        print("\n CONSISTENCY CHECK \n")

        print("Running second pass for consistency validation...\n")

        second_run_state = run_multi_agent_system(business_text)

        first_report = final_state["final_report"]["report"]
        second_report = second_run_state["final_report"]["report"]

        consistency_result = run_consistency_check(first_report, second_report)

        print(
            f"Consistency Score: {consistency_result['consistency_score_percent']}%"
        )   