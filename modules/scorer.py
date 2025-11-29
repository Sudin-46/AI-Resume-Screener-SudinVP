import re

def compute_scores(resume_text, jd, llm_analysis=None):
    resume_low = resume_text.lower()
    jd_skills = jd.get('skills', [])
    
    # Find matched skills
    matched = [s for s in jd_skills if s in resume_low]
    skills_score = (len(matched) / max(1, len(jd_skills))) * 100 if jd_skills else 0

    # Extract experience from resume text
    experience = 1
    m = re.search(r"(\d+)\+?\s+years?", resume_text, re.I)
    if m:
        experience = int(m.group(1))

    # Experience score (simple rule)
    experience_score = min(100, experience * 10)

    # ATS score calculation
    ats_score = (0.6 * skills_score) + (0.4 * experience_score)

    # LLM analysis
    summary = None
    fit_score = None
    
    if llm_analysis:
        summary = llm_analysis.get("summary")
        fit_score = llm_analysis.get("fit_score")

    if not summary:
        summary = resume_text[:600] + "..." if len(resume_text) > 600 else resume_text

    return {
        "skills_match": matched,
        "skills_score": skills_score,
        "experience_score": experience_score,
        "ats_score": ats_score,
        "summary": summary,
        "fit_score": fit_score
    }
