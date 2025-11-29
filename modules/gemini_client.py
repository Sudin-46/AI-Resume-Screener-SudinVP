import requests

def gemini_available(api_key):
    return bool(api_key and len(api_key.strip()) > 0)

def analyze_with_gemini(resume_text, jd_text, api_key, api_url_prefix):
    """
    Sends resume + job description to Google Gemini API.
    """
    # Build the full URL
    if api_url_prefix.endswith('='):
        url = api_url_prefix + api_key
    else:
        url = api_url_prefix

    headers = {"Content-Type": "application/json"}

    payload = {
        "prompt": {
            "text": build_prompt(resume_text, jd_text)
        },
        "maxOutputTokens": 512
    }

    response = requests.post(url, json=payload, headers=headers, timeout=20)

    if response.status_code != 200:
        raise RuntimeError(f"Gemini API Error: {response.text}")

    data = response.json()

    # Try extracting summary from Gemini output
    try:
        candidates = data.get("candidates", [])
        if candidates:
            content = candidates[0].get("content", "")
            return {"summary": content, "fit_score": 75}
    except:
        pass

    # fallback
    return {
        "summary": response.text,
        "fit_score": 75
    }

def build_prompt(resume_text, jd_text):
    return (
        "Analyze the following resume against the job description. "
        "Give a summary and estimate a fit_score out of 100.\n\n"
        "Job Description:\n" + jd_text + "\n\nResume:\n" + resume_text
    )
