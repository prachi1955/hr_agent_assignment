import os
import re
import pdfplumber
import docx

def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def extract_resume_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".docx", ".doc"]:
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def parse_resume(file_path: str) -> dict:
    text = extract_resume_text(file_path)
    text_lower = text.lower()

    name = "Unknown"
    for line in text.split("\n"):
        line = line.strip()
        if len(line) > 2 and len(line) < 50 and not any(c.isdigit() for c in line):
            name = line
            break

    email_match = re.search(r'[\w.-]+@[\w.-]+\.\w+', text)
    email = email_match.group() if email_match else "N/A"

    all_skills = [
        "python", "java", "javascript", "typescript", "c++", "c#", "go", "ruby",
        "django", "fastapi", "flask", "spring", "react", "angular", "vue",
        "postgresql", "mysql", "mongodb", "redis", "sqlite",
        "docker", "kubernetes", "aws", "azure", "gcp",
        "git", "linux", "rest api", "graphql",
        "machine learning", "deep learning", "pandas", "numpy", "tensorflow",
        "pytest", "jenkins", "ci/cd", "celery"
    ]
    skills = [s for s in all_skills if s in text_lower]

    exp_match = re.search(r'(\d+)\+?\s*year', text_lower)
    experience_years = int(exp_match.group(1)) if exp_match else 0

    domain = "Software Engineering"
    if any(w in text_lower for w in ["data science", "machine learning", "ai", "deep learning"]):
        domain = "Data Science / AI"
    elif any(w in text_lower for w in ["finance", "accounting", "banking"]):
        domain = "Finance"

    education = "Not specified"
    if "b.tech" in text_lower or "bachelor" in text_lower or "b.e" in text_lower:
        education = "Bachelor's Degree"
    if "m.tech" in text_lower or "master" in text_lower or "mba" in text_lower:
        education = "Master's Degree"
    if "phd" in text_lower or "doctorate" in text_lower:
        education = "PhD"

    certs = []
    if "aws certified" in text_lower:
        certs.append("AWS Certified")
    if "azure" in text_lower and "certif" in text_lower:
        certs.append("Azure Certified")
    if "google cloud" in text_lower and "certif" in text_lower:
        certs.append("GCP Certified")
    if "pmp" in text_lower:
        certs.append("PMP")

    project_count = len(re.findall(r'project', text_lower))
    projects = [f"Project reference #{i+1}" for i in range(min(project_count, 5))]

    word_count = len(text.split())
    if word_count > 400:
        comm = "excellent"
    elif word_count > 200:
        comm = "adequate"
    else:
        comm = "poor"

    return {
        "name": name,
        "email": email,
        "skills": skills,
        "total_experience_years": experience_years,
        "experience_domains": [domain],
        "education": education,
        "certifications": certs,
        "projects": projects,
        "communication_quality": comm,
        "summary": f"{name} | {experience_years} yrs exp | Skills: {', '.join(skills[:4]) if skills else 'None detected'}",
        "file": os.path.basename(file_path),
        "raw_text_preview": text[:300]
    }