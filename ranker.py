def rank_candidates(scored_candidates: list) -> list:
    sorted_candidates = sorted(
        scored_candidates,
        key=lambda x: x["weighted_total"],
        reverse=True
    )
    for i, candidate in enumerate(sorted_candidates, start=1):
        candidate["rank"] = i
    return sorted_candidates