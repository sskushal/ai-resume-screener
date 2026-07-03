"""
app.py
Streamlit UI for the AI Resume Screener / Job Matcher.

Run locally with:
    streamlit run app.py
"""

import streamlit as st
from matcher import extract_text, score_resume, get_llm_feedback

st.set_page_config(page_title="AI Resume Screener", page_icon="🧠", layout="wide")

st.title("🧠 AI Resume Screener / Job Matcher")
st.caption(
    "Upload a resume and paste a job description to get a match score, "
    "matched/missing skills, and optional AI-generated feedback."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Resume")
    resume_file = st.file_uploader(
        "Upload resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"]
    )

with col2:
    st.subheader("💼 Job Description")
    jd_text_input = st.text_area("Paste the job description here", height=250)

with st.expander("⚙️ Optional: Enable LLM-based feedback (OpenAI API)"):
    api_key = st.text_input("OpenAI API Key", type="password")
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"], index=0)
    st.caption(
        "Leave the key blank to use the free, fully offline TF-IDF + "
        "skill-matching engine only."
    )

analyze = st.button("🔍 Analyze Match", type="primary")

if analyze:
    if not resume_file:
        st.error("Please upload a resume file.")
    elif not jd_text_input.strip():
        st.error("Please paste a job description.")
    else:
        with st.spinner("Extracting text and scoring..."):
            resume_bytes = resume_file.read()
            try:
                resume_text = extract_text(resume_bytes, resume_file.name)
            except Exception as e:
                st.error(f"Could not read resume file: {e}")
                st.stop()

            result = score_resume(resume_text, jd_text_input)

        st.markdown("---")
        st.subheader("📊 Match Results")

        score_col, skill_col, sem_col = st.columns(3)
        score_col.metric("Overall Match Score", f"{result['final_score']}%")
        skill_col.metric("Skill Match", f"{result['skill_score']}%")
        sem_col.metric("Semantic Similarity", f"{result['semantic_score']}%")

        st.progress(min(int(result["final_score"]), 100) / 100)

        m_col, mi_col = st.columns(2)
        with m_col:
            st.markdown("### ✅ Matched Skills")
            if result["matched_skills"]:
                st.write(", ".join(result["matched_skills"]))
            else:
                st.write("No overlapping skills detected.")

        with mi_col:
            st.markdown("### ❌ Missing Skills (in JD, not in resume)")
            if result["missing_skills"]:
                st.write(", ".join(result["missing_skills"]))
            else:
                st.write("None — great coverage!")

        if api_key:
            st.markdown("---")
            st.subheader("🤖 AI Feedback")
            with st.spinner("Asking the LLM for detailed feedback..."):
                feedback = get_llm_feedback(resume_text, jd_text_input, api_key, model)
            st.markdown(feedback)

        st.markdown("---")
        report = f"""AI Resume Screener Report
==========================
Overall Match Score: {result['final_score']}%
Skill Match Score: {result['skill_score']}%
Semantic Similarity Score: {result['semantic_score']}%

Matched Skills:
{', '.join(result['matched_skills']) or 'None'}

Missing Skills:
{', '.join(result['missing_skills']) or 'None'}
"""
        st.download_button(
            "⬇️ Download Report (TXT)", report, file_name="match_report.txt"
        )
