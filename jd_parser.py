import re

def parse_jd(jd_text: str) -> dict:
    text_lower = jd_text.lower()

    all_skills = [
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "ruby",
        "django", "fastapi", "flask", "spring", "react", "angular", "vue",
        "postgresql", "mysql", "mongodb", "redis", "sqlite",
        "docker", "kubernetes", "aws", "azure", "gcp",
        "git", "linux", "rest api", "graphql",
        "machine learning", "deep learning", "pandas", "numpy", "tensorflow",
        "pytest", "jenkins", "ci/cd", "celery"
    ]

    required_skills = [s for s in all_skills if s in text_lower]

    exp_match = re.search(r'(\d+)\s*[-–to]+\s*(\d+)\s*year', text_lower)
    min_exp = int(exp_match.group(1)) if exp_match else 0

    domain = "Software Engineering"
    if any(w in text_lower for w in ["data science", "machine learning", "deep learning", "ai"]):
        domain = "Data Science / AI"
    elif any(w in text_lower for w in ["finance", "accounting", "credit"]):
        domain = "Finance"
    elif any(w in text_lower for w in ["marketing", "seo", "content"]):
        domain = "Marketing"

    title = "Software Developer"
    for line in jd_text.split("\n"):
        if "title" in line.lower() or "role" in line.lower() or "position" in line.lower():
            title = line.split(":")[-1].strip()
            break

    education = "Any degree"
    if "b.tech" in text_lower or "bachelor" in text_lower:
        education = "Bachelor's Degree"
    if "m.tech" in text_lower or "master" in text_lower:
        education = "Master's Degree"

    certs = []
    if "aws" in text_lower and "certif" in text_lower:
        certs.append("AWS Certification")
    if "azure" in text_lower and "certif" in text_lower:
        certs.append("Azure Certification")

    return {
        "job_title": title,
        "required_skills": required_skills,
        "preferred_skills": [],
        "min_experience_years": min_exp,
        "education_requirement": education,
        "certifications": certs,
        "domain": domain
    }