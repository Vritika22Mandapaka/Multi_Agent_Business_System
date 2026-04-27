def get_market_context():
    """
    Simulated web search results for MVP demo.
    Later this can be replaced with Tavily, SerpAPI, or real API search.
    """

    return {
        "market_trends": [
            "Growing adoption of AI-powered personalization in grocery delivery",
            "College students prefer convenience-based subscription services",
            "High demand for budget-friendly smart grocery planning"
        ],
        "competitors": [
            "Instacart",
            "GoPuff",
            "Amazon Fresh",
            "Walmart Grocery"
        ],
        "external_risks": [
            "High delivery logistics costs",
            "Data privacy concerns",
            "Thin operating margins",
            "Strong competition from existing delivery giants"
        ]
    }