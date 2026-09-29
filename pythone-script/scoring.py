WEIGHTS = {
    "long_function": 5,
    "unused_import": 3,
}


def scoring_system(result: dict) -> tuple[float, dict[str, float]]:
    """
    Evaluates a file's analyzer result and calculates a health score.

    Args:
        result (dict): Per-file result from analyzer.analyze(), containing
            "issues" — a list of issue dicts, each with a "type" key.

    Returns:
        tuple: (total_score, score_breakdown), where score_breakdown maps
        each issue type to the total points it cost.
    """
    issue_counts = {}
    for issue in result["issues"]:
        issue_type = issue["type"]
        issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1

    score_breakdown = {}

    long_function_count = issue_counts.get("long_function", 0)
    score_breakdown["long_function"] = long_function_count * WEIGHTS["long_function"]

    unused_import_count = issue_counts.get("unused_import", 0)
    billable_imports = max(0, unused_import_count - 1)  
    score_breakdown["unused_import"] = billable_imports * WEIGHTS["unused_import"]

    total_penalty = sum(score_breakdown.values())
    total_score = max(0.0, min(100.0, 100.0 - total_penalty))
    return(print(score_breakdown,total_score ))





