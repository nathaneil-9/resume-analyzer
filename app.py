# app.py

from parser import extract_text_from_pdf
from skill_extractor import extract_skills
from matcher import (
    match_resume_to_job,
    find_missing_skills,
    find_matched_skills
)

pdf_path = "sample_resume.pdf"

job_description = """
Looking for a candidate with experience in Python, Machine Learning,
SQL, and Data Analysis. Familiarity with Linux is a plus.
"""

# Step 1: Extract resume text
text = extract_text_from_pdf(pdf_path)

# Step 2: Extract skills
skills = extract_skills(text)

# Step 3: Match score
score = match_resume_to_job(text, job_description)

# Step 4: Skill comparison
missing_skills = find_missing_skills(text, job_description)
matched_skills = find_matched_skills(text, job_description)

# Output
print("\n===== DETECTED SKILLS =====\n")
print(skills)

print("\n===== MATCH SCORE =====\n")
print(f"{score}%")

print("\n===== MATCHED SKILLS =====\n")
print(matched_skills)

print("\n===== MISSING SKILLS =====\n")
print(missing_skills)

from matcher import skill_match_score

skill_score = skill_match_score(text, job_description)

print("\n===== SKILL MATCH SCORE =====\n")
print(f"{skill_score}%")

final_score = (0.4 * score) + (0.6 * skill_score)

print("\n===== FINAL SCORE =====\n")
print(f"{round(final_score, 2)}%")