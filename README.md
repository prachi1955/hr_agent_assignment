#  HR Resume Shortlisting Agent

An AI-assisted HR Resume Shortlisting System built using Python and Streamlit.  
The system automatically parses Job Descriptions (JD) and resumes, evaluates candidates on multiple dimensions, ranks them, and generates an HTML shortlist report.

---

#  Project Overview

The HR Resume Shortlisting Agent helps recruiters automate the initial candidate screening process.

The application:
- Parses Job Descriptions
- Extracts resume information from PDF/DOCX files
- Matches candidate skills with JD requirements
- Scores candidates using weighted evaluation metrics
- Ranks applicants automatically
- Allows HR overrides for manual adjustments
- Generates downloadable HTML reports

The project is fully rule-based and does not require API keys.

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core backend logic |
| Streamlit | Frontend UI |
| Jinja2 | HTML report generation |
| PyPDF2 / pdfplumber | PDF parsing |
| python-docx | DOCX parsing |

---

#  Project Structure

```bash
hr_assignment/
│
├── app/
│   ├── __init__.py
│   ├── jd_parser.py
│   ├── resume_parser.py
│   ├── scorer.py
│   ├── ranker.py
│   ├── report_generator.py
│   └── override.py
│
├── data/
│   ├── resumes/
│   └── sample_jd.txt
│
├── outputs/
│   ├── results.json
│   └── shortlist_report.html
│
├── ui.py
├── main.py
├── requirements.txt
└── README.md
