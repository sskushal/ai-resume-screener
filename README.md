# AI Resume Screener / Job Matcher

An AI-powered tool that scores how well a resume matches a job description,
highlights matched and missing skills, and optionally generates LLM-based
qualitative feedback.

## Features
- Upload resume as **PDF, DOCX, or TXT**
- Paste any **job description**
- Keyword-based **skill extraction** across 150+ technical skills (ML/AI,
  web dev, cloud, databases, tools)
- **TF-IDF cosine similarity** for semantic/contextual matching (works fully
  offline — no API key needed)
- Combined **weighted match score** (skill overlap + semantic similarity)
- Optional **LLM feedback** (OpenAI API) with strengths, gaps, and rewrite
  suggestions
- Downloadable match report

## How it works
1. **Text extraction** — pulls raw text from the uploaded resume file.
2. **Skill extraction** — matches known technical skills against a curated
   skills database using regex word-boundary matching.
3. **Scoring**:
   - *Skill Match Score* = (skills in both resume & JD) / (skills in JD)
   - *Semantic Similarity Score* = TF-IDF cosine similarity between full
     resume and JD text
   - *Final Score* = weighted blend (default: 60% skill match, 40% semantic)
4. **(Optional) LLM Feedback** — if an OpenAI API key is provided, sends the
   resume + JD to the model for a qualitative recruiter-style review.

## Setup

\`\`\`bash
cd resume_screener
pip install -r requirements.txt
streamlit run app.py
\`\`\`

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## Project Structure
\`\`\`
resume_screener/
├── app.py              # Streamlit UI
├── matcher.py           # Core scoring logic (extraction, skills, similarity, LLM)
├── skills_db.py          # Curated technical skills database
├── requirements.txt
├── sample_data/
│   ├── sample_resume.txt
│   └── sample_jd.txt
└── README.md
\`\`\`

## Testing without the UI
\`\`\`python
from matcher import score_resume

resume_text = open("sample_data/sample_resume.txt").read()
jd_text = open("sample_data/sample_jd.txt").read()

result = score_resume(resume_text, jd_text)
print(result)
\`\`\`

## Tech Stack
Python, Streamlit, scikit-learn (TF-IDF + cosine similarity), PyPDF2,
python-docx, OpenAI API (optional)

## Possible Extensions
- Swap TF-IDF for sentence-transformer embeddings for deeper semantic matching
- Batch-score multiple resumes against one JD and rank candidates
- Add a "resume rewrite suggestions" mode that rewrites bullet points to
  better match the JD's keywords (ATS optimization)
