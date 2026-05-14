import streamlit as st
import os
import json
import tempfile

from app.jd_parser import parse_jd
from app.resume_parser import parse_resume
from app.scorer import score_candidate
from app.ranker import rank_candidates
from app.report_generator import generate_report
from app.override import apply_override

st.set_page_config(page_title="HR Shortlisting Agent", page_icon="📋", layout="wide")

st.title("📋 HR Resume Shortlisting Agent")
st.caption("Rule-based scoring · No API key needed · Human-in-the-Loop")

# ── Inputs directly on main page (not sidebar) ──
st.subheader("Step 1 — Paste Job Description")
jd_text = st.text_area("Job Description", height=200, placeholder="Paste JD here...")

st.subheader("Step 2 — Upload Resumes")
resume_files = st.file_uploader("Upload PDF or DOCX resumes", type=["pdf","docx"], accept_multiple_files=True)

st.subheader("Step 3 — Run")
run_btn = st.button("🚀 Run Shortlisting", type="primary")

if "ranked" not in st.session_state:
    st.session_state.ranked = []
if "jd" not in st.session_state:
    st.session_state.jd = {}

if run_btn:
    if not jd_text.strip():
        st.error("Please paste a Job Description.")
    elif not resume_files:
        st.error("Please upload at least one resume.")
    else:
        with st.spinner("Parsing JD..."):
            jd = parse_jd(jd_text)
            st.session_state.jd = jd
        st.success(f"✅ JD Parsed: **{jd['job_title']}**")

        candidates = []
        for f in resume_files:
            suffix = ".pdf" if f.name.endswith(".pdf") else ".docx"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(f.read())
                tmp_path = tmp.name
            with st.spinner(f"Parsing {f.name}..."):
                try:
                    c = parse_resume(tmp_path)
                    candidates.append(c)
                    st.write(f"✅ Parsed: **{c.get('name','Unknown')}** | Skills found: {len(c['skills'])}")
                except Exception as e:
                    st.warning(f"⚠️ Could not parse {f.name}: {e}")

        scored = []
        for c in candidates:
            result = score_candidate(jd, c)
            scored.append(result)

        ranked = rank_candidates(scored)
        st.session_state.ranked = ranked
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/results.json", "w") as f:
            json.dump({"jd": jd, "candidates": ranked}, f, indent=2)
        generate_report(jd, ranked)
        st.success("✅ Done! Scroll down to see results.")

if st.session_state.ranked:
    ranked = st.session_state.ranked
    jd = st.session_state.jd

    st.divider()
    st.subheader(f"🏆 Results — {len(ranked)} Candidate(s)")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total", len(ranked))
    c2.metric("✅ HIRE", sum(1 for c in ranked if c["hire_recommendation"]=="HIRE"))
    c3.metric("🟡 MAYBE", sum(1 for c in ranked if c["hire_recommendation"]=="MAYBE"))
    c4.metric("❌ NO HIRE", sum(1 for c in ranked if c["hire_recommendation"]=="NO HIRE"))

    for c in ranked:
        badge = {"HIRE":"🟢","MAYBE":"🟡","NO HIRE":"🔴"}.get(c["hire_recommendation"],"⚪")
        with st.expander(f"#{c['rank']} {badge} {c['candidate_name']} — {c['weighted_total']}/10 — {c['hire_recommendation']}", expanded=(c['rank']==1)):
            st.caption(c.get("candidate_summary",""))

            col1,col2,col3,col4,col5 = st.columns(5)
            for col, key, label, w in [
                (col1,"skills_match","Skills Match","30%"),
                (col2,"experience_relevance","Experience","25%"),
                (col3,"education_certs","Education","15%"),
                (col4,"project_portfolio","Projects","20%"),
                (col5,"communication_quality","Comms","10%"),
            ]:
                col.metric(f"{label} ({w})", f"{c[key]['score']}/10")
                col.caption(c[key]['justification'])

            st.markdown("---")
            st.markdown("**🖊️ HR Override**")
            o1, o2, o3 = st.columns(3)
            with o1:
                dim = st.selectbox("Dimension", ["skills_match","experience_relevance","education_certs","project_portfolio","communication_quality"], key=f"d_{c['candidate_name']}")
            with o2:
                new_score = st.slider("New Score", 0, 10, int(c[dim]["score"]), key=f"s_{c['candidate_name']}")
            with o3:
                reason = st.text_input("Reason", key=f"r_{c['candidate_name']}")
            if st.button("Apply Override", key=f"b_{c['candidate_name']}"):
                if reason.strip():
                    updated = apply_override(c, dim, new_score, reason)
                    idx = next(i for i,x in enumerate(st.session_state.ranked) if x["candidate_file"]==c["candidate_file"])
                    st.session_state.ranked[idx] = updated
                    st.session_state.ranked = rank_candidates(st.session_state.ranked)
                    generate_report(jd, st.session_state.ranked)
                    st.rerun()
                else:
                    st.warning("Please enter a reason.")

    st.divider()
    if os.path.exists("outputs/shortlist_report.html"):
        with open("outputs/shortlist_report.html","rb") as f:
            st.download_button("⬇️ Download HTML Report", f, file_name="shortlist_report.html", mime="text/html", use_container_width=True)