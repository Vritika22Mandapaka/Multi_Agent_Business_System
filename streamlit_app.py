import os
import sys
import tempfile

import fitz
import streamlit as st

from evals.consistency_check import run_consistency_check
from evals.rubric_eval import run_rubric_evaluation
from rag.extract_state import extract_state


def extract_text_from_pdf(uploaded_file):
    text = ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    try:
        doc = fitz.open(temp_path)
        try:
            for page in doc:
                text += page.get_text()
        finally:
            doc.close()
    finally:
        os.remove(temp_path)

    return text.strip()


def run_multi_agent_system(business_text):
    from app.graph import build_graph

    app = build_graph()
    target_state = extract_state(business_text)
    initial_state = {
        "business_idea": business_text,
        "research_output": None,
        "tech_output": None,
        "finance_output": None,
        "retry_output": None,
        "final_report": None,
        "target_state": target_state,
        "regulatory_context": None,
    }
    return app.invoke(initial_state)


def main():
    st.set_page_config(
        page_title="AI Multi-Agent Business Decision System",
        page_icon=":robot_face:",
        layout="wide",
    )

    st.sidebar.caption(f"Python: {sys.executable}")
    st.title("AI Multi-Agent Business Decision System")
    st.write(
        "Upload a business idea as a PDF/TXT file or type it manually. "
        "The system will run Research, Technology, Finance, Retry, and Synthesis agents."
    )

    tab1, tab2 = st.tabs(["Upload File", "Type Business Idea"])
    business_text = ""

    with tab1:
        uploaded_file = st.file_uploader("Upload PDF or TXT file", type=["pdf", "txt"])
        if uploaded_file:
            if uploaded_file.name.endswith(".pdf"):
                business_text = extract_text_from_pdf(uploaded_file)
            else:
                business_text = uploaded_file.read().decode("utf-8").strip()

            st.subheader("Input Preview")
            st.text_area("Business Idea Text", business_text, height=200)

    with tab2:
        typed_text = st.text_area(
            "Enter your business idea",
            height=200,
            placeholder=(
                "Example: I want to launch an AI-powered grocery delivery startup "
                "for college students in New Jersey..."
            ),
        )
        if typed_text.strip():
            business_text = typed_text.strip()

    if st.button("Run Multi-Agent Analysis"):
        if not business_text:
            st.error("Please upload a file or type a business idea first.")
            return

        with st.spinner("Running multi-agent analysis..."):
            final_state = run_multi_agent_system(business_text)

        st.success("Analysis completed.")
        detected_state = final_state.get("target_state")
        if detected_state:
            st.info(
                f"Detected State: **{detected_state}**. "
                "Regulatory compliance context was included in the synthesis when available."
            )
        else:
            st.warning("No Northeast US state detected. Regulatory compliance context was skipped.")

        st.header("Final Business Decision Report")
        st.markdown(final_state["final_report"]["report"])

        st.header("Agent Outputs")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Research Agent")
            st.write(final_state["research_output"]["analysis"])
        with col2:
            st.subheader("Technology Agent")
            st.write(final_state["tech_output"]["analysis"])
        with col3:
            st.subheader("Finance Agent")
            st.write(final_state["finance_output"]["analysis"])

        if final_state.get("retry_output"):
            st.header("Retry Agent Output")
            st.write(final_state["retry_output"]["analysis"])

        st.header("Rubric-Based Evaluation")
        evaluation_results = run_rubric_evaluation(final_state)
        for agent, result in evaluation_results.items():
            st.write(f"**{agent}:** {result['score']} / {result['total']}")
            if result["missing"]:
                st.warning(f"Missing: {', '.join(result['missing'])}")

        st.header("Consistency Check")
        with st.spinner("Running second pass for consistency validation..."):
            second_run_state = run_multi_agent_system(business_text)

        consistency_result = run_consistency_check(
            final_state["final_report"]["report"],
            second_run_state["final_report"]["report"],
        )
        st.metric(
            label="Consistency Score",
            value=f"{consistency_result['consistency_score_percent']}%",
        )


if __name__ == "__main__":
    main()
