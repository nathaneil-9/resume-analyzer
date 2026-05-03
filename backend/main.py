from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

from backend.parser import extract_text_from_pdf
from backend.skill_extractor import extract_skills
from backend.matcher import (
    match_resume_to_job,
    skill_match_score,
    find_missing_skills,
    find_matched_skills
)

app = FastAPI()

# 🔥 Enable CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
def test():
    print("🔥 TEST HIT 🔥")
    return {"message": "working"}


@app.post("/analyze/")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    print("🔥 FUNCTION CALLED 🔥")
    sys.stdout.flush()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    temp_path = os.path.join(BASE_DIR, f"temp_{file.filename}")

    # Save uploaded file
    contents = await file.read()
    with open(temp_path, "wb") as buffer:
        buffer.write(contents)

    # Extract text
    text = extract_text_from_pdf(temp_path)

    print("TEXT LENGTH:", len(text))
    print("TEXT PREVIEW:", text[:300])

    # Core processing
    skills = extract_skills(text)
    tfidf_score = match_resume_to_job(text, job_description)
    skill_score = skill_match_score(text, job_description)
    final_score = round((0.4 * tfidf_score) + (0.6 * skill_score), 2)

    matched = find_matched_skills(text, job_description)
    missing = find_missing_skills(text, job_description)

    # 🔥 Suggestions feature
    suggestions = [
        f"Consider learning or adding '{skill}' to your resume"
        for skill in missing
    ]

    # Delete temp file
    os.remove(temp_path)

    return {
        "detected_skills": skills,
        "tfidf_score": tfidf_score,
        "skill_score": skill_score,
        "final_score": final_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions
    }