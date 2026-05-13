import os
import fitz
from datetime import datetime
from fpdf import FPDF
from dotenv import load_dotenv
from evals.rubric_eval import run_rubric_evaluation
from app.graph import build_graph
from evals.consistency_check import run_consistency_check
from rag.extract_state import extract_state


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


def export_to_pdf(final_state, consistency_result, evaluation_results, business_text):
    import re
    from fpdf.enums import XPos, YPos

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    NX = XPos.LMARGIN
    NY = YPos.NEXT

    def section_title(text):
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_fill_color(30, 30, 60)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, text, new_x=NX, new_y=NY, fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)

    def body(text):
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, str(text), new_x=NX, new_y=NY)
        pdf.ln(1)

    def label_value(label, value):
        pdf.set_font("Helvetica", "B", 10)
        pdf.multi_cell(0, 6, f"{label} {value}", new_x=NX, new_y=NY)

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(30, 30, 60)
    pdf.multi_cell(0, 12, "AI Multi-Agent Business Decision Report", align="C", new_x=NX, new_y=NY)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 6, datetime.now().strftime("%B %d, %Y  %I:%M %p"), align="C", new_x=NX, new_y=NY)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    section_title("Business Idea")
    body(business_text)

    # Research Agent
    section_title("Research Agent Output")
    r = final_state.get("research_output", {})
    body(r.get("analysis", "Not available"))

    # Finance Agent
    section_title("Finance Agent Output")
    f = final_state.get("finance_output", {})
    fp = f.get("extracted_parameters", {})
    fc = f.get("calculator_results", {})
    fs = f.get("structured", {})

    body("--- Extracted Financial Parameters ---")
    label_value("Startup Costs:", f"${fp.get('startup_costs', 0):,.0f}")
    label_value("Total Investment:", f"${fp.get('total_investment', 0):,.0f}")
    label_value("Revenue per Unit:", f"${fp.get('revenue_per_unit', 0):,.2f}")
    label_value("Variable Cost per Unit:", f"${fp.get('variable_cost_per_unit', 0):,.2f}")
    label_value("Monthly Fixed Costs:", f"${fp.get('monthly_fixed_costs', 0):,.0f}")
    label_value("Projected Year 1 Revenue:", f"${fp.get('projected_year1_revenue', 0):,.0f}")
    label_value("Monthly Profit at Scale:", f"${fp.get('monthly_profit_at_scale', 0):,.0f}")
    pdf.ln(2)
    body("--- Calculator Results ---")
    label_value("Contribution per Unit:", f"${fc.get('contribution_per_unit', 0):,.2f}")
    label_value("Projected Year 1 Profit:", f"${fc.get('projected_year1_profit', 0):,.0f}")
    label_value("Break-Even Units/Month:", str(fc.get('break_even_units_per_month', 'N/A')))
    label_value("Year 1 ROI:", f"{fc.get('year1_roi_percent', 'N/A')}%")
    label_value("Payback Period:", f"{fc.get('payback_period_months', 'N/A')} months")
    pdf.ln(2)
    body("--- Financial Analysis ---")
    for key, lbl in [
        ("startup_costs", "Startup Costs:"),
        ("monthly_operating_costs", "Operating Costs:"),
        ("revenue_model", "Revenue Model:"),
        ("roi_projection", "ROI Projection:"),
        ("break_even_analysis", "Break-Even:"),
        ("payback_period", "Payback Period:"),
        ("confidence_reasoning", "Confidence Reasoning:"),
    ]:
        label_value(lbl, fs.get(key, ""))
    label_value("Confidence Score:", f"{fs.get('confidence_score', '')}/100")
    pdf.ln(2)
    body("Financial Risks:")
    for risk in fs.get("financial_risks", []):
        body(f"  - {risk}")

    # Tech Agent
    section_title("Technical Agent Output")
    t = final_state.get("tech_output", {})
    req = t.get("project_requirements", {})
    arch = t.get("systems_architecture", {})
    effort = t.get("development_effort", {})
    ops = t.get("operational_requirements", {})

    label_value("Feasibility Verdict:", t.get("feasibility_verdict", ""))
    pdf.ln(2)
    body("--- Tech Stack ---")
    label_value("Frontend:", ", ".join(req.get("frontend", [])))
    label_value("Backend:", ", ".join(req.get("backend", [])))
    label_value("Database:", ", ".join(req.get("database", [])))
    label_value("AI/ML Stack:", ", ".join(req.get("ai_ml_stack", [])))
    label_value("APIs & Tools:", ", ".join(req.get("apis_tools", [])))
    pdf.ln(2)
    body("--- Infrastructure ---")
    label_value("Cloud Services:", ", ".join(req.get("cloud_services", [])))
    label_value("Deployment:", ", ".join(req.get("deployment_requirements", [])))
    label_value("Scalability:", ", ".join(req.get("scalability_requirements", [])))
    label_value("Monitoring:", ", ".join(req.get("monitoring_logging", [])))
    pdf.ln(2)
    body("--- Systems Architecture ---")
    label_value("Style:", arch.get("architecture_style", ""))
    label_value("Key Components:", ", ".join(arch.get("key_components", [])))
    label_value("Security:", ", ".join(arch.get("security_architecture", [])))
    pdf.ln(2)
    body("--- Implementation Plan ---")
    label_value("MVP Timeline:", effort.get("mvp_timeline", ""))
    label_value("Full Timeline:", effort.get("estimated_timeline", ""))
    label_value("Team Size:", effort.get("recommended_team_size", ""))
    label_value("Roles:", ", ".join(effort.get("required_roles", [])))
    label_value("Complexity:", effort.get("complexity_level", ""))
    pdf.ln(2)
    body("--- Operational Requirements ---")
    label_value("Compliance:", ", ".join(ops.get("compliance_requirements", [])))
    label_value("Reliability:", ", ".join(ops.get("reliability_requirements", [])))
    label_value("Maintenance:", ", ".join(ops.get("maintenance_needs", [])))
    pdf.ln(2)
    body("Technical Risks:")
    for risk in t.get("technical_risks", []):
        body(f"  - {risk}")
    label_value("Confidence Score:", f"{t.get('confidence_score', '')}/100")
    pdf.ln(2)
    body("Reasoning Summary:")
    body(t.get("reasoning_summary", ""))

    # Final Report
    section_title("Final Business Decision Report")
    body(final_state.get("final_report", {}).get("report", "Not available"))

    # Rubric Evaluation
    section_title("Rubric-Based Evaluation")
    for agent, result in evaluation_results.items():
        pdf.set_font("Helvetica", "B", 10)
        pdf.multi_cell(0, 6, f"{agent}: {result['score']} / {result['total']}", new_x=NX, new_y=NY)
        if result["missing"]:
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 6, f"  Missing: {', '.join(result['missing'])}", new_x=NX, new_y=NY)
    pdf.ln(2)

    # Consistency
    section_title("Consistency Check")
    body(f"Consistency Score: {consistency_result['consistency_score_percent']}%")

    slug = re.sub(r"[^a-zA-Z0-9\s]", "", business_text)
    slug = "_".join(slug.split()[:6])
    filename = f"{slug}.pdf"
    pdf.output(filename)
    return filename


def run_multi_agent_system(business_text, target_state=None):
    app = build_graph()

    initial_state = {
        "business_idea": business_text,
        "target_state": target_state,
        "research_output": None,
        "tech_output": None,
        "tech_eval": None,
        "finance_output": None,
        "retry_output": None,
        "final_report": None,
        "regulatory_context": None
    }

    final_state = app.invoke(initial_state)

    return final_state


if __name__ == "__main__":
    print("\n   AI Multi-Agent Business Decision System \n")

    business_text = load_business_input()

    if business_text:
        print("\nInput Loaded Successfully")

        target_state = extract_state(business_text)
        if target_state:
            print(f"Detected state: {target_state} — regulatory compliance section will be included.")

        print("\nRunning Multi-Agent Analysis...\n")

        final_state = run_multi_agent_system(business_text, target_state=target_state)

        print("\n  RESEARCH AGENT OUTPUT \n")
        r = final_state["research_output"]
        print(r.get("analysis", "No analysis available."))

        print("\n  FINANCE AGENT OUTPUT \n")
        f = final_state["finance_output"]
        fc = f.get("calculator_results", {})
        fp = f.get("extracted_parameters", {})
        fs = f.get("structured", {})

        print("Extracted Financial Parameters:")
        print(f"  Startup Costs:            ${fp.get('startup_costs', 0):,.0f}")
        print(f"  Total Investment:         ${fp.get('total_investment', 0):,.0f}")
        print(f"  Revenue per Unit:         ${fp.get('revenue_per_unit', 0):,.2f}")
        print(f"  Variable Cost per Unit:   ${fp.get('variable_cost_per_unit', 0):,.2f}")
        print(f"  Monthly Fixed Costs:      ${fp.get('monthly_fixed_costs', 0):,.0f}")
        print(f"  Projected Year 1 Revenue: ${fp.get('projected_year1_revenue', 0):,.0f}")
        print(f"  Monthly Profit at Scale:  ${fp.get('monthly_profit_at_scale', 0):,.0f}")

        print("\nCalculator Results:")
        print(f"  Contribution per Unit:    ${fc.get('contribution_per_unit', 0):,.2f}")
        print(f"  Projected Year 1 Profit:  ${fc.get('projected_year1_profit', 0):,.0f}")
        print(f"  Break-Even Units/Month:   {fc.get('break_even_units_per_month', 'N/A')}")
        print(f"  Year 1 ROI:               {fc.get('year1_roi_percent', 'N/A')}%")
        print(f"  Payback Period:           {fc.get('payback_period_months', 'N/A')} months")

        print("\nFinancial Analysis:")
        print(f"  Startup Costs:      {fs.get('startup_costs', '')}")
        print(f"  Operating Costs:    {fs.get('monthly_operating_costs', '')}")
        print(f"  Revenue Model:      {fs.get('revenue_model', '')}")
        print(f"  ROI Projection:     {fs.get('roi_projection', '')}")
        print(f"  Break-Even:         {fs.get('break_even_analysis', '')}")
        print(f"  Payback Period:     {fs.get('payback_period', '')}")
        print(f"  Confidence Score:   {fs.get('confidence_score', '')}/100")
        print(f"  Confidence Reason:  {fs.get('confidence_reasoning', '')}")

        print("\nFinancial Risks:")
        for risk in fs.get("financial_risks", []):
            print(f"  - {risk}")

        print("\n  TECHNICAL AGENT OUTPUT \n")
        t = final_state["tech_output"]
        req = t.get("project_requirements", {})
        arch = t.get("systems_architecture", {})
        effort = t.get("development_effort", {})
        ops = t.get("operational_requirements", {})

        print(f"Feasibility Verdict: {t.get('feasibility_verdict', '')}\n")

        print("Tech Stack:")
        print(f"  Frontend:           {', '.join(req.get('frontend', []))}")
        print(f"  Backend:            {', '.join(req.get('backend', []))}")
        print(f"  Database:           {', '.join(req.get('database', []))}")
        print(f"  AI/ML Stack:        {', '.join(req.get('ai_ml_stack', []))}")
        print(f"  APIs & Tools:       {', '.join(req.get('apis_tools', []))}")

        print("\nInfrastructure:")
        print(f"  Cloud Services:     {', '.join(req.get('cloud_services', []))}")
        print(f"  Deployment:         {', '.join(req.get('deployment_requirements', []))}")
        print(f"  Scalability:        {', '.join(req.get('scalability_requirements', []))}")
        print(f"  Monitoring:         {', '.join(req.get('monitoring_logging', []))}")

        print("\nSystems Architecture:")
        print(f"  Style:              {arch.get('architecture_style', '')}")
        print(f"  Key Components:     {', '.join(arch.get('key_components', []))}")
        print(f"  Security:           {', '.join(arch.get('security_architecture', []))}")

        print("\nImplementation Plan:")
        print(f"  MVP Timeline:       {effort.get('mvp_timeline', '')}")
        print(f"  Full Timeline:      {effort.get('estimated_timeline', '')}")
        print(f"  Team Size:          {effort.get('recommended_team_size', '')}")
        print(f"  Roles:              {', '.join(effort.get('required_roles', []))}")
        print(f"  Phases:             {' | '.join(effort.get('development_phases', []))}")
        print(f"  Complexity:         {effort.get('complexity_level', '')}")

        print("\nOperational Requirements:")
        print(f"  Compliance:         {', '.join(ops.get('compliance_requirements', []))}")
        print(f"  Reliability:        {', '.join(ops.get('reliability_requirements', []))}")
        print(f"  Maintenance:        {', '.join(ops.get('maintenance_needs', []))}")

        print("\nTechnical Risks:")
        for risk in t.get("technical_risks", []):
            print(f"  - {risk}")

        print(f"\nSecurity Requirements:  {', '.join(req.get('security_requirements', []))}")
        print(f"Confidence Score:       {t.get('confidence_score', '')}/100")
        print(f"\nReasoning Summary:\n{t.get('reasoning_summary', '')}")

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

        second_run_state = run_multi_agent_system(business_text, target_state=target_state)

        first_report = final_state["final_report"]["report"]
        second_report = second_run_state["final_report"]["report"]

        consistency_result = run_consistency_check(first_report, second_report)

        print(
            f"Consistency Score: {consistency_result['consistency_score_percent']}%"
        )

        export = input("\nWould you like to export the report as a PDF? (yes/no): ").strip().lower()
        if export in ("yes", "y"):
            filename = export_to_pdf(final_state, consistency_result, evaluation_results, business_text)
            print(f"Report saved as: {filename}")