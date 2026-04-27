def compare_outputs(output1, output2):
    text1 = output1.lower()
    text2 = output2.lower()

    common_keywords = [
        "market",
        "competitor",
        "risk",
        "feasibility",
        "roi",
        "break-even",
        "recommendation",
        "confidence"
    ]

    matched = 0

    for keyword in common_keywords:
        if keyword in text1 and keyword in text2:
            matched += 1

    consistency_score = (matched / len(common_keywords)) * 100

    return round(consistency_score, 2)


def run_consistency_check(report_run_1, report_run_2):
    score = compare_outputs(report_run_1, report_run_2)

    return {
        "consistency_score_percent": score
    }