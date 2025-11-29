import re

COMMON_TECH = [
    "java", "core java", "spring", "spring boot", "spring-boot", "springboot",
    "rest", "rest api", "restful", "mysql", "postgresql", "sql", "oracle",
    "mongodb", "nosql", "git", "maven", "gradle", "docker", "kubernetes",
    "aws", "azure", "gcp", "html", "css", "javascript", "react", "angular",
    "node", "python", "c++", "c#", "oop", "data structures", "algorithms",
    "hibernate", "jpa"
]

def normalize_token(s):
    return re.sub(r'[^a-z0-9#+-]', ' ', s.lower()).strip()

def parse_job_description(jd_text):
    text = jd_text or ''
    text_low = text.lower()
    found = set()

    # Match known technologies
    for tech in COMMON_TECH:
        if tech in text_low:
            found.add(tech)

    # Detect uppercase technologies like REST, API, Git
    caps = re.findall(r'\b[A-Za-z0-9+#\-]{2,30}\b', jd_text)
    for token in caps:
        tnorm = normalize_token(token)
        if tnorm in COMMON_TECH:
            found.add(tnorm)

    skills = sorted(list(found))

    # Extract minimum required experience
    m = re.search(r'(\d+)\+?\s+years?', jd_text, re.I)
    min_years = int(m.group(1)) if m else 0

    # First non-empty line = title
    first_line = ""
    for line in jd_text.splitlines():
        if line.strip():
            first_line = line.strip()
            break

    return {
        'title': first_line or "Job",
        'skills': skills,
        'min_years': min_years,
        'raw': jd_text
    }
