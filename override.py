import json
import os
from datetime import datetime

OVERRIDE_LOG = "outputs/override_log.json"

def load_overrides() -> list:
    if os.path.exists(OVERRIDE_LOG):
        with open(OVERRIDE_LOG, "r") as f:
            return json.load(f)
    return []

def save_overrides(overrides: list):
    os.makedirs("outputs", exist_ok=True)
    with open(OVERRIDE_LOG, "w") as f:
        json.dump(overrides, f, indent=2)

def apply_override(candidate: dict, dimension: str, new_score: int, reason: str) -> dict:
    from app.scorer import WEIGHTS

    old_score = candidate[dimension]["score"]
    candidate[dimension]["score"] = new_score
    candidate[dimension]["justification"] += f" [HR OVERRIDE: {reason}]"

    candidate["weighted_total"] = round(
        candidate["skills_match"]["score"] * WEIGHTS["skills_match"] +
        candidate["experience_relevance"]["score"] * WEIGHTS["experience_relevance"] +
        candidate["education_certs"]["score"] * WEIGHTS["education_certs"] +
        candidate["project_portfolio"]["score"] * WEIGHTS["project_portfolio"] +
        candidate["communication_quality"]["score"] * WEIGHTS["communication_quality"],
        2
    )

    overrides = load_overrides()
    overrides.append({
        "timestamp": datetime.now().isoformat(),
        "candidate": candidate["candidate_name"],
        "dimension": dimension,
        "old_score": old_score,
        "new_score": new_score,
        "reason": reason,
        "new_total": candidate["weighted_total"]
    })
    save_overrides(overrides)
    return candidate