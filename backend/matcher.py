from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.skill_extractor import extract_skills


# 🔹 TF-IDF similarity
def match_resume_to_job(resume_text, job_description):
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    return round(similarity[0][0] * 100, 2)


# 🔥 Filter job skills
def filter_job_skills(job_skills):
    meaningful = []

    KEYWORDS = [
        "marketing", "seo", "analytics", "media", "campaign",
        "data", "learning", "management", "python", "sql",
        "machine", "analysis", "sales", "communication",
        "social", "content", "branding", "research",
        "education", "child", "care", "teaching", "support"
    ]

    for skill in job_skills:
        words = skill.split()

        if 1 <= len(words) <= 3:
            if any(k in skill for k in KEYWORDS):
                meaningful.append(skill)

    return list(set(meaningful))


# 🔥 Synonyms for better matching
SYNONYMS = {
    "childcare": ["children", "kids", "child care"],
    "counseling": ["support", "guidance"],
    "special needs": ["disability", "special needs support"],
    "education": ["teaching", "school", "learning"],
    "communication": ["interaction", "speaking"],
    "management": ["supervision", "handling"],
    "coordination": ["organizing", "planning"]
}


# 🔥 Smart matching
def match_lists(resume_skills, job_skills):
    matched = []

    for job_skill in job_skills:
        for resume_skill in resume_skills:

            job_words = set(job_skill.split())
            resume_words = set(resume_skill.split())

            # direct match
            if job_words.intersection(resume_words):
                matched.append(job_skill)
                break

            # synonym match
            for key, values in SYNONYMS.items():
                if key in job_skill:
                    if any(v in resume_skill for v in values):
                        matched.append(job_skill)
                        break

    return list(set(matched))


# 🔹 Matched skills
def find_matched_skills(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    job_skills = filter_job_skills(job_skills)

    return match_lists(resume_skills, job_skills)


# 🔹 Missing skills
def find_missing_skills(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    job_skills = filter_job_skills(job_skills)

    matched = match_lists(resume_skills, job_skills)

    return [s for s in job_skills if s not in matched]


# 🔥 Smart weighted scoring
def skill_match_score(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    job_skills = filter_job_skills(job_skills)
    matched = match_lists(resume_skills, job_skills)

    if not job_skills:
        return 0

    total_weight = 0
    matched_weight = 0

    jd_lower = job_description.lower()

    for skill in job_skills:
        weight = 1

        if "required" in jd_lower or "must" in jd_lower:
            weight = 2
        elif "preferred" in jd_lower or "plus" in jd_lower:
            weight = 0.5

        total_weight += weight

        if skill in matched:
            matched_weight += weight

    score = (matched_weight / total_weight) * 100

    return round(score, 2)