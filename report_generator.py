import os
from datetime import datetime
from jinja2 import Template

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HR Shortlist Report</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', sans-serif; background: #f4f6f9; color: #1a1a2e; padding: 40px; }
  h1 { font-size: 2rem; margin-bottom: 6px; }
  .meta { color: #666; font-size: 0.9rem; margin-bottom: 30px; }
  .jd-box { background: #fff; border-left: 4px solid #4361ee; padding: 16px 20px; border-radius: 8px; margin-bottom: 30px; }
  .jd-box h2 { font-size: 1.1rem; color: #4361ee; margin-bottom: 8px; }
  .card { background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.07); }
  .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
  .rank-badge { background: #4361ee; color: white; border-radius: 50%; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; font-weight: bold; }
  .name { font-size: 1.25rem; font-weight: 700; }
  .email { color: #888; font-size: 0.85rem; }
  .total { font-size: 1.8rem; font-weight: 800; color: #4361ee; }
  .rec { padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
  .HIRE { background: #d4edda; color: #155724; }
  .MAYBE { background: #fff3cd; color: #856404; }
  .NO-HIRE { background: #f8d7da; color: #721c24; }
  .dims { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-top: 16px; }
  .dim { background: #f8f9ff; border-radius: 8px; padding: 12px; border-left: 3px solid #4361ee; }
  .dim-name { font-size: 0.7rem; text-transform: uppercase; color: #888; }
  .dim-score { font-size: 1.4rem; font-weight: 800; }
  .dim-just { font-size: 0.78rem; color: #555; margin-top: 4px; }
  .bar-bg { background: #e9ecef; border-radius: 4px; height: 6px; margin-top: 6px; }
  .bar { background: #4361ee; height: 6px; border-radius: 4px; }
  .summary { font-style: italic; color: #666; font-size: 0.88rem; margin-top: 4px; }
  footer { text-align: center; color: #aaa; font-size: 0.8rem; margin-top: 40px; }
</style>
</head>
<body>
<h1>📋 HR Shortlist Report</h1>
<p class="meta">Generated: {{ generated_at }} | Job: <strong>{{ jd.job_title }}</strong> | {{ candidates|length }} candidate(s)</p>

<div class="jd-box">
  <h2>Job Requirements</h2>
  <p><strong>Domain:</strong> {{ jd.domain }} | <strong>Min Experience:</strong> {{ jd.min_experience_years }} yrs | <strong>Education:</strong> {{ jd.education_requirement }}</p>
  <p style="margin-top:6px;"><strong>Required Skills:</strong> {{ jd.required_skills | join(', ') }}</p>
</div>

{% for c in candidates %}
<div class="card">
  <div class="card-header">
    <div style="display:flex;align-items:center;gap:14px;">
      <div class="rank-badge">#{{ c.rank }}</div>
      <div>
        <div class="name">{{ c.candidate_name }}</div>
        <div class="email">{{ c.candidate_email }} | {{ c.candidate_file }}</div>
        <div class="summary">{{ c.candidate_summary }}</div>
      </div>
    </div>
    <div style="text-align:right;">
      <div class="total">{{ c.weighted_total }}/10</div>
      <span class="rec {{ c.hire_recommendation | replace(' ', '-') }}">{{ c.hire_recommendation }}</span>
    </div>
  </div>
  <div class="dims">
    {% for dim, label, weight in [
      ('skills_match','Skills Match','30%'),
      ('experience_relevance','Experience','25%'),
      ('education_certs','Education','15%'),
      ('project_portfolio','Projects','20%'),
      ('communication_quality','Communication','10%')
    ] %}
    <div class="dim">
      <div class="dim-name">{{ label }} ({{ weight }})</div>
      <div class="dim-score">{{ c[dim].score }}/10</div>
      <div class="bar-bg"><div class="bar" style="width:{{ c[dim].score * 10 }}%"></div></div>
      <div class="dim-just">{{ c[dim].justification }}</div>
    </div>
    {% endfor %}
  </div>
</div>
{% endfor %}
<footer>HR Shortlisting Agent — AI-assisted, human-reviewed</footer>
</body>
</html>
"""

def generate_report(jd: dict, ranked_candidates: list, output_path: str = "outputs/shortlist_report.html"):
    os.makedirs("outputs", exist_ok=True)
    template = Template(HTML_TEMPLATE)
    html = template.render(
        jd=jd,
        candidates=ranked_candidates,
        generated_at=datetime.now().strftime("%d %b %Y, %I:%M %p")
    )
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Report saved to {output_path}")
    return output_path