import json
from pydantic import BaseModel, Field
from typing import List, Dict, Any

from app.llm_client import call_llm


# -----------------------------
# Pydantic Schemas
# -----------------------------

class ProjectRequirements(BaseModel):
    frontend: List[str]
    backend: List[str]
    database: List[str]
    ai_ml_stack: List[str]
    cloud_services: List[str]
    apis_tools: List[str]
    security_requirements: List[str]
    deployment_requirements: List[str]
    scalability_requirements: List[str]
    monitoring_logging: List[str]


class SystemsArchitecture(BaseModel):
    architecture_style: str
    key_components: List[str]
    data_flow: List[str]
    security_architecture: List[str]


class DevelopmentEffort(BaseModel):
    estimated_timeline: str
    mvp_timeline: str
    recommended_team_size: str
    required_roles: List[str]
    development_phases: List[str]
    complexity_level: str


class OperationalRequirements(BaseModel):
    maintenance_needs: List[str]
    compliance_requirements: List[str]
    reliability_requirements: List[str]


class TechnicalAgentOutput(BaseModel):
    feasibility_verdict: str
    project_requirements: ProjectRequirements
    systems_architecture: SystemsArchitecture
    development_effort: DevelopmentEffort
    operational_requirements: OperationalRequirements
    technical_risks: List[str]
    confidence_score: int = Field(ge=0, le=100)
    reasoning_summary: str


# -----------------------------
# Prompt Variants
# -----------------------------

ZERO_SHOT_PROMPT = """
You are the Technical Planning Agent in a multi-agent business decision system.

You reason like a full technical team — covering tech stack selection, infrastructure planning, systems architecture, implementation planning, and operational requirements — and produce ONE structured response.

Answer the question: "What would a real technical team need in order to successfully build and scale this business idea?"

Cover ALL of the following dimensions:

1. TECH STACK: Frontend, backend, database, AI/ML stack, APIs and third-party tools
2. INFRASTRUCTURE: Cloud services, hosting, deployment, storage, scalability, monitoring and logging
3. SYSTEMS ARCHITECTURE: Architecture style (monolith / microservices / serverless / event-driven), key components, data flow, security architecture
4. IMPLEMENTATION PLANNING: Team roles, timeline, MVP timeline, development phases, complexity
5. OPERATIONAL PLANNING: Maintenance needs, compliance requirements (GDPR, HIPAA, PCI-DSS if applicable), reliability requirements

Use the Research Agent output to tailor recommendations to the specific market context.

Business Idea:
{business_idea}

Research Agent Output:
{research_output}

Return ONLY valid JSON using this exact structure:

{{
    "feasibility_verdict": "",

    "project_requirements": {{
        "frontend": [],
        "backend": [],
        "database": [],
        "ai_ml_stack": [],
        "cloud_services": [],
        "apis_tools": [],
        "security_requirements": [],
        "deployment_requirements": [],
        "scalability_requirements": [],
        "monitoring_logging": []
    }},

    "systems_architecture": {{
        "architecture_style": "",
        "key_components": [],
        "data_flow": [],
        "security_architecture": []
    }},

    "development_effort": {{
        "estimated_timeline": "",
        "mvp_timeline": "",
        "recommended_team_size": "",
        "required_roles": [],
        "development_phases": [],
        "complexity_level": ""
    }},

    "operational_requirements": {{
        "maintenance_needs": [],
        "compliance_requirements": [],
        "reliability_requirements": []
    }},

    "technical_risks": [],

    "confidence_score": 0,

    "reasoning_summary": ""
}}

Rules:
- Return ONLY JSON
- No markdown, no explanations outside JSON
- Each list must contain specific, detailed items — not generic one-word answers
- Confidence score must be between 0 and 100
- reasoning_summary must be 3-5 sentences covering key architectural decisions and trade-offs
"""


FEW_SHOT_PROMPT = """
You are the Technical Planning Agent in a multi-agent business decision system.

You reason like a full technical team — covering tech stack selection, infrastructure planning, systems architecture, implementation planning, and operational requirements — and produce ONE structured response.

Answer the question: "What would a real technical team need in order to successfully build and scale this business idea?"

Example:

Business Idea:
AI-powered telemedicine platform for rural primary care — connects patients with licensed doctors via video, handles prescriptions digitally, and integrates with insurance providers.

Research Agent Output:
Strong demand in underserved rural markets. Key competitors include Teladoc and MDLive. Regulatory compliance and insurance integration are major friction points.

Example Output:
{{
    "feasibility_verdict": "Technically Feasible with Significant Compliance Overhead",

    "project_requirements": {{
        "frontend": ["React Native (iOS + Android)", "React.js (patient and doctor web portals)", "Offline-capable PWA for low-connectivity rural areas"],
        "backend": ["Node.js with Express (API layer)", "Python FastAPI (AI/ML services)", "WebRTC signaling server for video sessions"],
        "database": ["PostgreSQL (patient records, appointments)", "Redis (real-time session caching)", "TimescaleDB (health metrics time-series data)"],
        "ai_ml_stack": ["Symptom triage classification model (scikit-learn)", "NLP for clinical note summarization (HuggingFace)", "OpenAI API for doctor-assist Q&A"],
        "cloud_services": ["AWS GovCloud (HIPAA-eligible)", "AWS RDS Multi-AZ (database)", "AWS S3 with server-side encryption (file storage)", "AWS CloudFront (CDN for low-latency video)"],
        "apis_tools": ["Twilio Video API (video consultations)", "Stripe API (billing)", "Surescripts API (e-prescriptions)", "Availity API (insurance eligibility verification)"],
        "security_requirements": ["HIPAA Business Associate Agreements with all vendors", "End-to-end encryption for all PHI in transit and at rest", "OAuth 2.0 + MFA for all accounts", "Full audit logging for all PHI access"],
        "deployment_requirements": ["Docker + Kubernetes (EKS)", "CI/CD pipeline with automated compliance checks", "Blue-green deployment for zero-downtime releases", "Dedicated staging environment mirroring production"],
        "scalability_requirements": ["Auto-scaling ECS clusters for video session spikes", "Queue-based async processing for prescription workflows", "Multi-region failover for 99.9% uptime SLA"],
        "monitoring_logging": ["AWS CloudWatch (infrastructure metrics)", "Datadog (application performance monitoring)", "Full audit trail for HIPAA compliance", "PagerDuty (on-call alerting)"]
    }},

    "systems_architecture": {{
        "architecture_style": "Microservices architecture with event-driven communication between services",
        "key_components": ["API Gateway (routing and rate limiting)", "Auth Service (OAuth2 + MFA)", "Video Session Service (WebRTC)", "Prescription Service", "Insurance Verification Service", "AI Triage Service", "Notification Service"],
        "data_flow": ["Patient submits symptoms → AI triage → Doctor queue assignment", "Doctor joins session → WebRTC peer connection via signaling server", "Prescription issued → Surescripts API → Pharmacy fulfillment"],
        "security_architecture": ["JWT tokens with short expiry for session management", "Role-based access control (patient, doctor, admin)", "All PHI encrypted at rest with AES-256", "VPC isolation for all backend services"]
    }},

    "development_effort": {{
        "estimated_timeline": "12-16 months for full platform",
        "mvp_timeline": "5-6 months for basic video consultation and booking",
        "recommended_team_size": "10-12 members",
        "required_roles": ["Backend Engineer (HIPAA/healthcare API experience)", "Mobile Engineer (React Native)", "Frontend Engineer (React.js)", "ML Engineer (triage model)", "DevOps/Cloud Engineer (AWS)", "Security Engineer", "UI/UX Designer", "QA Engineer", "Project Manager"],
        "development_phases": ["Phase 1 (MVP): User auth, doctor profiles, video consultation, basic booking", "Phase 2: Prescription integration, insurance verification, AI triage", "Phase 3: Multi-state expansion, analytics dashboard, mobile app polish"],
        "complexity_level": "High"
    }},

    "operational_requirements": {{
        "maintenance_needs": ["24/7 on-call rotation for platform incidents", "Monthly HIPAA compliance audits", "Quarterly penetration testing", "Ongoing model retraining as clinical data grows"],
        "compliance_requirements": ["HIPAA (patient data)", "State medical licensing compliance per region", "SOC 2 Type II certification for enterprise clients"],
        "reliability_requirements": ["99.9% uptime SLA", "Multi-region active-passive failover", "Automated database backups every 6 hours", "Disaster recovery RTO under 4 hours"]
    }},

    "technical_risks": [
        "HIPAA compliance requirements constrain every vendor and data flow decision",
        "WebRTC video quality degrades significantly in low-bandwidth rural areas",
        "Insurance eligibility APIs vary widely by payer — integration complexity is underestimated",
        "State-by-state medical licensing creates regulatory complexity for multi-state rollout"
    ],

    "confidence_score": 74,

    "reasoning_summary": "The platform is buildable using proven healthcare cloud infrastructure on AWS GovCloud, but HIPAA compliance dominates every architectural decision and significantly extends the timeline. A microservices architecture is the right choice here because each domain (video, prescriptions, insurance) has distinct scaling needs and compliance boundaries. The hardest unsolved technical problem is reliable video delivery in low-bandwidth rural areas — adaptive bitrate streaming and a WebRTC fallback strategy are essential. A phased rollout starting in one state before expanding nationally reduces both regulatory and integration risk."
}}

Now analyze the following:

Business Idea:
{business_idea}

Research Agent Output:
{research_output}

Return ONLY valid JSON. Match the depth and specificity of the example above.
"""


CHAIN_OF_THOUGHT_PROMPT = """
You are the Technical Planning Agent in a multi-agent business decision system.

You reason like a full technical team — covering tech stack selection, infrastructure planning, systems architecture, implementation planning, and operational requirements — and produce ONE structured response.

Answer the question: "What would a real technical team need in order to successfully build and scale this business idea?"

Think through each of the following steps carefully. Capture your reasoning in the "reasoning_summary" field.

--- TECH STACK ---
Step 1: What frontend platforms are needed (web, mobile, both)? What frameworks fit this product?
Step 2: What backend architecture is needed? What AI/ML infrastructure does this product require?
Step 3: What databases and data storage are needed? Is real-time data involved?
Step 4: What third-party APIs and tools are essential (payments, maps, messaging, AI services)?

--- INFRASTRUCTURE ---
Step 5: What cloud services and hosting are required? What are the peak load scenarios from the Research Agent output?
Step 6: How will this be deployed and monitored? What does the CI/CD pipeline and observability stack look like?

--- SYSTEMS ARCHITECTURE ---
Step 7: What architecture style fits this product (monolith, microservices, serverless, event-driven)? What are the key system components and how do they interact?

--- IMPLEMENTATION PLANNING ---
Step 8: What team roles are needed? What is a realistic MVP timeline vs. full platform timeline? What are the development phases?

--- OPERATIONAL PLANNING ---
Step 9: What compliance requirements apply (GDPR, HIPAA, PCI-DSS)? What are the long-term maintenance and reliability needs?

--- RISKS ---
Step 10: What are the 3-4 most likely technical failure points or integration challenges specific to this business idea?

Business Idea:
{business_idea}

Research Agent Output:
{research_output}

Return ONLY valid JSON using this exact structure:

{{
    "feasibility_verdict": "",

    "project_requirements": {{
        "frontend": [],
        "backend": [],
        "database": [],
        "ai_ml_stack": [],
        "cloud_services": [],
        "apis_tools": [],
        "security_requirements": [],
        "deployment_requirements": [],
        "scalability_requirements": [],
        "monitoring_logging": []
    }},

    "systems_architecture": {{
        "architecture_style": "",
        "key_components": [],
        "data_flow": [],
        "security_architecture": []
    }},

    "development_effort": {{
        "estimated_timeline": "",
        "mvp_timeline": "",
        "recommended_team_size": "",
        "required_roles": [],
        "development_phases": [],
        "complexity_level": ""
    }},

    "operational_requirements": {{
        "maintenance_needs": [],
        "compliance_requirements": [],
        "reliability_requirements": []
    }},

    "technical_risks": [],

    "confidence_score": 0,

    "reasoning_summary": ""
}}

Rules:
- Return ONLY JSON
- No markdown, no explanations outside JSON
- Each list must contain specific, detailed items — not generic one-word answers
- Confidence score must be between 0 and 100
- reasoning_summary must be 3-5 sentences covering the key architectural decisions and trade-offs
"""


# -----------------------------
# Prompt Selector
# -----------------------------

def build_prompt(
    prompt_type: str,
    business_idea: str,
    research_output: Dict[str, Any]
) -> str:

    prompt_map = {
        "zero_shot": ZERO_SHOT_PROMPT,
        "few_shot": FEW_SHOT_PROMPT,
        "cot": CHAIN_OF_THOUGHT_PROMPT
    }

    selected_prompt = prompt_map.get(prompt_type, CHAIN_OF_THOUGHT_PROMPT)

    return selected_prompt.format(
        business_idea=business_idea,
        research_output=json.dumps(research_output, indent=2)
    )


# -----------------------------
# Rubric Evaluation
# -----------------------------

def evaluate_technical_output(output: Dict[str, Any]) -> Dict[str, Any]:

    score = 0
    checks = {}

    checks["feasibility_verdict"] = bool(output.get("feasibility_verdict"))

    req = output.get("project_requirements", {})
    checks["frontend"] = bool(req.get("frontend"))
    checks["backend"] = bool(req.get("backend"))
    checks["database"] = bool(req.get("database"))
    checks["ai_ml_stack"] = bool(req.get("ai_ml_stack"))
    checks["monitoring_logging"] = bool(req.get("monitoring_logging"))

    arch = output.get("systems_architecture", {})
    checks["architecture_style"] = bool(arch.get("architecture_style"))
    checks["key_components"] = bool(arch.get("key_components"))

    effort = output.get("development_effort", {})
    checks["development_effort"] = bool(effort)
    checks["development_phases"] = bool(effort.get("development_phases"))

    checks["operational_requirements"] = bool(output.get("operational_requirements"))
    checks["technical_risks"] = bool(output.get("technical_risks"))
    checks["confidence_score"] = isinstance(output.get("confidence_score"), int)

    for value in checks.values():
        if value:
            score += 1

    return {
        "rubric_score": score,
        "max_score": len(checks),
        "checks": checks
    }


# -----------------------------
# Main Technical Agent
# -----------------------------

def tech_agent(state, prompt_type="cot"):

    business_idea = state["business_idea"]
    research_output = state.get("research_output", {})

    prompt = build_prompt(
        prompt_type=prompt_type,
        business_idea=business_idea,
        research_output=research_output
    )

    result = call_llm(prompt, temperature=0.2)

    try:
        parsed_result = json.loads(result)

        validated_result = TechnicalAgentOutput(**parsed_result)

        evaluation = evaluate_technical_output(parsed_result)

        r = validated_result
        req = r.project_requirements
        arch = r.systems_architecture
        effort = r.development_effort
        ops = r.operational_requirements

        analysis = "\n".join([
            f"Feasibility: {r.feasibility_verdict}",
            f"\nTech Stack:",
            f"  Frontend: {', '.join(req.frontend)}",
            f"  Backend: {', '.join(req.backend)}",
            f"  Database: {', '.join(req.database)}",
            f"  AI/ML: {', '.join(req.ai_ml_stack)}",
            f"  APIs/Tools: {', '.join(req.apis_tools)}",
            f"\nArchitecture: {arch.architecture_style}",
            f"Key Components: {', '.join(arch.key_components)}",
            f"\nDevelopment: {effort.mvp_timeline} MVP | {effort.estimated_timeline} full platform",
            f"Team: {effort.recommended_team_size} — {', '.join(effort.required_roles)}",
            f"Complexity: {effort.complexity_level}",
            f"\nCompliance: {', '.join(ops.compliance_requirements)}",
            f"Reliability: {', '.join(ops.reliability_requirements)}",
            f"\nTechnical Risks: {'; '.join(r.technical_risks)}",
            f"\nConfidence Score: {r.confidence_score}/100",
            f"\nReasoning: {r.reasoning_summary}",
        ])

        output = validated_result.model_dump()
        output["analysis"] = analysis

        return {
            "tech_output": output,
            "tech_eval": evaluation
        }

    except Exception as e:

        return {
            "tech_output": {
                "error": "Failed to parse technical agent output",
                "exception": str(e),
                "raw_output": result
            },
            "tech_eval": {
                "rubric_score": 0,
                "max_score": 13,
                "checks": {}
            }
        }


# -----------------------------
# Consistency Check
# -----------------------------

def consistency_check(state, runs=3):

    outputs = []

    for _ in range(runs):
        result = tech_agent(state, prompt_type="cot")
        outputs.append(result["tech_output"])

    return outputs
