def detect_business_domain(text: str) -> str:
    """
    Simple keyword-based business domain detector.
    Used to decide whether domain-specific Market RAG should be applied.
    """

    if not text:
        return "general"

    text = text.lower()

    grocery_keywords = [
        "grocery",
        "groceries",
        "food delivery",
        "supermarket",
        "cart",
        "shopping cart",
        "meal planning",
        "weekly groceries",
        "delivery startup",
        "student grocery",
    ]

    education_keywords = [
        "school",
        "preschool",
        "daycare",
        "childcare",
        "kindergarten",
        "education",
        "early childhood",
        "tutoring",
        "students learning",
        "classroom",
    ]

    healthcare_keywords = [
        "clinic",
        "hospital",
        "patient",
        "medical",
        "healthcare",
        "doctor",
        "therapy",
        "mental health",
    ]

    finance_keywords = [
        "bank",
        "banking",
        "investment",
        "fintech",
        "loan",
        "credit",
        "insurance",
        "trading",
    ]

    if any(keyword in text for keyword in grocery_keywords):
        return "grocery"

    if any(keyword in text for keyword in education_keywords):
        return "education"

    if any(keyword in text for keyword in healthcare_keywords):
        return "healthcare"

    if any(keyword in text for keyword in finance_keywords):
        return "finance"

    return "general"