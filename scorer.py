WEIGHTS = {
    "skills_match": 0.30,
    "experience_relevance": 0.25,
    "education_certs": 0.15,
    "project_portfolio": 0.20,
    "communication_quality": 0.10,
}

def score_candidate(jd: dict, candidate: dict) -> dict:

    # ── 1. Skills Match (30%) ─────────────────────────────────────────
    jd_skills = [s.lower() for s in jd.get("required_skills", [])]
    candidate_skills = [s.lower() for s in candidate.get("skills", [])]

    if jd_skills:
        matched = len(set(jd_skills) & set(candidate_skills))
        match_pct = matched / len(jd_skills)
    else:
        match_pct = 0

    if match_pct >= 0.85:
        skills_score = 9
        skills_just = f"Matched {int(match_pct*100)}% of required skills — excellent fit."
    elif match_pct >= 0.5:
        skills_score = 6
        skills_just = f"Matched {int(match_pct*100)}% of required skills — decent overlap."
    elif match_pct >= 0.3:
        skills_score = 3
        skills_just = f"Matched {int(match_pct*100)}% of required skills — low overlap."
    else:
        skills_score = 1
        skills_just = f"Matched {int(match_pct*100)}% of required skills — very poor fit."

    # ── 2. Experience Relevance (25%) ─────────────────────────────────
    required_exp = jd.get("min_experience_years", 0)
    candidate_exp = candidate.get("total_experience_years", 0)
    jd_domain = jd.get("domain", "").lower()
    candidate_domains = [d.lower() for d in candidate.get("experience_domains", [])]
    domain_match = any(jd_domain in d or d in jd_domain for d in candidate_domains)

    if candidate_exp >= required_exp and domain_match:
        exp_score = 9
        exp_just = f"{candidate_exp} yrs in matching domain — strong fit."
    elif candidate_exp >= required_exp and not domain_match:
        exp_score = 6
        exp_just = f"{candidate_exp} yrs experience but domain differs from JD."
    elif candidate_exp >= required_exp * 0.7:
        exp_score = 5
        exp_just = f"{candidate_exp} yrs — slightly below required {required_exp} yrs."
    else:
        exp_score = 2
        exp_just = f"Only {candidate_exp} yrs — well below required {required_exp} yrs."

    # ── 3. Education & Certifications (15%) ───────────────────────────
    education = candidate.get("education", "").lower()
    certs = candidate.get("certifications", [])

    if "phd" in education:
        edu_score = 10
        edu_just = "PhD — exceeds all education requirements."
    elif "master" in education:
        edu_score = 8
        edu_just = "Master's degree — exceeds minimum requirement."
    elif "bachelor" in education:
        edu_score = 6
        edu_just = "Bachelor's degree — meets minimum requirement."
    else:
        edu_score = 3
        edu_just = "Education qualification not clearly detected in resume."

    if certs:
        edu_score = min(10, edu_score + 1)
        edu_just += f" Has cert(s): {', '.join(certs)}."

    # ── 4. Project / Portfolio (20%) ──────────────────────────────────
    project_count = len(candidate.get("projects", []))

    if project_count >= 4:
        proj_score = 9
        proj_just = f"{project_count} project references found — strong portfolio."
    elif project_count >= 2:
        proj_score = 6
        proj_just = f"{project_count} project references found — moderate portfolio."
    elif project_count == 1:
        proj_score = 4
        proj_just = "Only 1 project reference found — limited portfolio."
    else:
        proj_score = 1
        proj_just = "No project references found in resume."

    # ── 5. Communication Quality (10%) ────────────────────────────────
    comm = candidate.get("communication_quality", "poor")
    if comm == "excellent":
        comm_score = 9
        comm_just = "Resume is well-structured with strong word count — excellent communication."
    elif comm == "adequate":
        comm_score = 6
        comm_just = "Resume has adequate length and structure."
    else:
        comm_score = 2
        comm_just = "Resume is very short or poorly structured."

    # ── Weighted Total ─────────────────────────────────────────────────
    weighted_total = round(
        skills_score * WEIGHTS["skills_match"] +
        exp_score * WEIGHTS["experience_relevance"] +
        edu_score * WEIGHTS["education_certs"] +
        proj_score * WEIGHTS["project_portfolio"] +
        comm_score * WEIGHTS["communication_quality"],
        2
    )

    # ── Hire Recommendation ────────────────────────────────────────────
    if weighted_total >= 7:
        recommendation = "HIRE"
    elif weighted_total >= 5:
        recommendation = "MAYBE"
    else:
        recommendation = "NO HIRE"

    return {
        "candidate_name": candidate.get("name", "Unknown"),
        "candidate_file": candidate.get("file", ""),
        "candidate_email": candidate.get("email", "N/A"),
        "candidate_summary": candidate.get("summary", ""),
        "skills_match": {"score": skills_score, "justification": skills_just},
        "experience_relevance": {"score": exp_score, "justification": exp_just},
        "education_certs": {"score": edu_score, "justification": edu_just},
        "project_portfolio": {"score": proj_score, "justification": proj_just},
        "communication_quality": {"score": comm_score, "justification": comm_just},
        "weighted_total": weighted_total,
        "hire_recommendation": recommendation
    }