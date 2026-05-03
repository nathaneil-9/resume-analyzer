# skill_extractor.py

import re
from backend.skills import SKILLS   # ✅ FIXED

def extract_skills(text):
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)

    found_skills = []

    for skill in SKILLS:
        # safer matching for short words
        if len(skill) <= 2:
            if skill in words:
                found_skills.append(skill)
        else:
            if skill in text:
                found_skills.append(skill)

    return list(set(found_skills))