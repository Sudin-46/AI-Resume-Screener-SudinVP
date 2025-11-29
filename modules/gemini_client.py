import requests

def gemini_available(api_key):
    return bool(api_key and len(api_key.strip()) > 0)

def analyze_with_gemini(resume_text, jd_text, api_key, api_url_prefix):
    # Correct final URL
    # Should look like:
    # https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_KEY
    url = api_url_prefix + api_key

    headers = {"Content-Type": "application/json"}

    prompt_text = build_prompt(resume_text, jd_text)

    # ✅ Correct Gemini API Payload Format
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 300
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)

        if response.status_code != 200:
            raise RuntimeError(f"Gemini API Error: {response.text}")

        data = response.json()
        
        # Extract output text safely
        text_output = (
            data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
        )

        if not text_output:
            return {
                "summary": "Gemini returned no usable text.",
                "fit_score": None
            }

        # Optional: Extract numeric fit score from model text
        extracted_score = extract_fit_score(text_output)

        return {
            "summary": text_output,
            "fit_score": extracted_score
        }

    except Exception as e:
        return {
            "summary": f"Gemini analysis failed: {str(e)}",
            "fit_score": None
        }


def extract_fit_score(model_text):
    """
    Tries to extract a number from the Gemini response.
    Defaults to 75 if nothing found.
    """
    import re
    numbers = re.findall(r"\b(\d{1,3})\b", model_text)
    for num in numbers:
        n = int(num)
        if 0 <= n <= 100:
            return n
    return 75


def build_prompt(resume_text, jd_text):
    return (
        "Analyze the following resume against the job description and provide:\n"
        "1. A short professional summary of the candidate.\n"
        "2. A fit score (0–100) based on match.\n\n"
        "Job Description:\n" + jd_text + "\n\n"
        "Resume:\n" + resume_text
    )
