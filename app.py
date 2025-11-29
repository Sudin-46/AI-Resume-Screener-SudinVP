import streamlit as st
from modules.parser import extract_text_from_pdf
from modules.jd import parse_job_description
from modules.scorer import compute_scores
from modules.gemini_client import analyze_with_gemini, gemini_available

st.set_page_config(page_title="Resume Screening Agent v10", layout="wide")
st.title("Resume Screening Agent")

with st.sidebar:
    st.header("Settings")
    gemini_key = st.text_input("Google API Key (from Cloud Console)", type="password")
    gemini_url = st.text_input("Gemini API URL",
        value="https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=")

jd_text_input = st.text_area("Paste Job Description Here", height=260)
resumes = st.file_uploader("Upload Resume(s) (PDF)", type=['pdf'], accept_multiple_files=True)

if st.button("Run Screening"):
    if not jd_text_input.strip():
        st.error("Please paste the job description.")
    elif not resumes:
        st.error("Please upload at least one resume PDF.")
    else:
        jd_text = jd_text_input.strip()
        jd = parse_job_description(jd_text)
        st.subheader("Job Description parsed")
        st.json(jd)

        results=[]
        for r in resumes:
            st.write(f"Processing **{r.name}** ...")
            resume_text = extract_text_from_pdf(r)
            if gemini_key and gemini_available(gemini_key):
                try:
                    llm_analysis = analyze_with_gemini(resume_text, jd_text, gemini_key, gemini_url)
                except Exception as e:
                    st.warning(f"Gemini analysis failed: {e}\nUsing local scoring.")
                    llm_analysis=None
            else:
                llm_analysis=None

            score=compute_scores(resume_text, jd, llm_analysis)
            results.append(dict(name=r.name, **score))
            st.success(f"Completed: {r.name}")

        st.header("Screening Results")
        for res in results:
            st.subheader(res['name'])
            st.metric("ATS Score", f"{res['ats_score']:.1f}%")
            st.write("**Skills match:**", res['skills_match'])
            st.write("**Skills score:**", f"{res['skills_score']:.1f}%")
            st.write("**Experience score:**", f"{res['experience_score']:.1f}%")
            st.write("**Fit score (LLM):**", res.get('fit_score',"N/A"))
            st.info(res['summary'])
            st.write("---")
