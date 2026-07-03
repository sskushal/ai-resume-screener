import re
import io
from typing import Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skills_db import ALL_SKILLS

def extract_text_from_pdf(file_bytes: bytes) -> str:
    from PyPDF2 import PdfReader
    reader = PdfReader(io.BytesIO(file_bytes))
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)


def extract_text_from_docx(file_bytes: bytes) -> str:
    import docx
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs)


def extract_text(file_bytes: bytes, filename: str) -> str:
    """Dispatch to the right extractor based on file extension."""
    filename = filename.lower()
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif filename.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file type: {filename}")

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+.#/\s-]", " ", text)  # keep tokens like c++, c#, node.js
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_skills(text: str) -> set:
    """Match known skills as whole phrases/words inside the cleaned text."""
    cleaned = clean_text(text)
    found = set()
    for skill in ALL_SKILLS:
        skill_clean = skill.lower()
        # word-boundary-safe match, but tolerant of symbols like c++, c#
        pattern = r"(?<![a-z0-9])" + re.escape(skill_clean) + r"(?![a-z0-9])"
        if re.search(pattern, cleaned):
            found.add(skill)
    return found

def compute_semantic_similarity(resume_text: str, jd_text: str) -> float:
    """TF-IDF cosine similarity between resume and JD, scaled to 0-100."""
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([clean_text(resume_text), clean_text(jd_text)])
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(sim * 100, 2)


def compute_skill_match(resume_skills: set, jd_skills: set) -> dict:
    if not jd_skills:
        return {"score": 0.0, "matched": [], "missing": []}
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    score = round(len(matched) / len(jd_skills) * 100, 2)
    return {
        "score": score,
        "matched": sorted(matched),
        "missing": sorted(missing),
    }


def score_resume(resume_text: str, jd_text: str,
                  skill_weight: float = 0.6, semantic_weight: float = 0.4) -> dict:
    """
    Combine skill-overlap score and semantic similarity into one final score.
    Default weighting favors exact skill matches (what most ATS/recruiters
    care about most) while still rewarding contextual/semantic overlap.
    """
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    skill_result = compute_skill_match(resume_skills, jd_skills)
    semantic_score = compute_semantic_similarity(resume_text, jd_text)

    final_score = round(
        skill_result["score"] * skill_weight + semantic_score * semantic_weight, 2
    )

    return {
        "final_score": final_score,
        "skill_score": skill_result["score"],
        "semantic_score": semantic_score,
        "matched_skills": skill_result["matched"],
        "missing_skills": skill_result["missing"],
        "resume_skills": sorted(resume_skills),
        "jd_skills": sorted(jd_skills),
    }
# ---------------------------------------------------------------------------

def get_llm_feedback(resume_text: str, jd_text: str, api_key: str,
                      model: str = "gpt-4o-mini") -> Optional[str]:
    """
    Calls an OpenAI-compatible chat completion endpoint to generate
    qualitative feedback: strengths, gaps, and rewrite suggestions.
    Returns None gracefully if the call fails (e.g., no internet / bad key)
    so the app degrades to the offline TF-IDF + skill-match score.
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        prompt = f"""You are an experienced technical recruiter. Compare this resume
against the job description and give concise, actionable feedback.

JOB DESCRIPTION:
{jd_text[:4000]}

RESUME:
{resume_text[:4000]}

Respond in this format:
1. Match Verdict (one line: Strong / Moderate / Weak fit)
2. Top 3 Strengths (bullet points)
3. Top 3 Gaps or Missing Skills (bullet points)
4. One specific suggestion to improve the resume for THIS job
"""
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[LLM feedback unavailable: {e}]"
