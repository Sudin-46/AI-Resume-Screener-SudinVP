import requests
import json
import re

def gemini_available(api_key):
    return bool(api_key and len(api_key.strip()) > 0)

def analyze_with_gemini(resume_text, jd_text, api_key, api_url_prefix):
    """
    Sends resume + job description to Google Gemini API (v1).
    Returns summary + fit_score or fallback.
    """

    # Build correct final URL
    url = api_url_prefix + api_key

    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": build_prompt(resume_text, jd_text)
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)

        if response.status_code != 200:
            raise RuntimeError(response.text)

        data = response.json()

        # Extract text from Gemini response
        text_output = (
            data["candidates"][0]["content"]["parts"][0]["text"]
        )

        # Extract fit score from the text
        score = extract_fit_score(text_output)

        return {
            "summary": text_output,
            "fit_score": score
        }

    except Exception as e:
        return {
            "summary": f"Gemini analysis failed → Using fallback.\n{str(e)}",
            "fit_score": 50   # fallback fit score so UI never shows None
        }


def extract_fit_score(text):
    """
    Extracts fit score (0–100) from model response.
    Returns 75 default if not found.
    """
    nums = re.findall(r"\b(\d{1,3})\b", text)
    for n in nums:
        n = int(n)
        if 0 <= n <= 100:
            return n
    return 75


def build_prompt(resume_text, jd_text):
    return (
        "Analyze the following resume against the job description.\n"
        "Respond ONLY in text. Include a fit score (0–100).\n\n"
        "Job Description:\n" + jd_text + "\n\n"
        "Resume:\n" + resume_text
    )

