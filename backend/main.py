from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.parser import extract_text_from_pdf
from backend.skill_extractor import extract_skills
from backend.matcher import (
    match_resume_to_job,
    skill_match_score,
    find_missing_skills,
    find_matched_skills
)

app = FastAPI()

# ✅ FIX 1: Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def is_low_signal(resume_text, detected_skills):
    return len(resume_text.split()) < 150 or len(detected_skills) < 5


def generate_suggestions(job_description):
    jd = job_description.lower()
    suggestions = []

    if "excel" in jd:
        suggestions.append("Add MS Excel skills or projects")

    if "typing" in jd:
        suggestions.append("Mention typing speed")

    if "communication" in jd:
        suggestions.append("Highlight communication skills")

    if "data" in jd or "entry" in jd:
        suggestions.append("Add data entry or computer experience")

    if "sales" in jd or "retail" in jd:
        suggestions.append("Mention sales or customer handling")

    if "child" in jd or "education" in jd:
        suggestions.append("Include childcare or teaching experience")

    if not suggestions:
        suggestions.append("Add a clear skills section")

    return suggestions


def generate_insight(matched, missing):
    if len(matched) == 0:
        return "No strong alignment found. Add key skills."

    if len(matched) > len(missing):
        return "Good match. Improve missing areas."

    return "Partial match. Improve skills."


@app.post("/analyze/")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    temp_path = os.path.join(BASE_DIR, f"temp_{file.filename}")

    try:
        # Save file
        contents = await file.read()
        with open(temp_path, "wb") as f:
            f.write(contents)

        # Extract text
        text = extract_text_from_pdf(temp_path)

        # Process
        skills = extract_skills(text)

        tfidf_score = match_resume_to_job(text, job_description)
        skill_score = skill_match_score(text, job_description)
        final_score = round((0.4 * tfidf_score) + (0.6 * skill_score), 2)

        matched = find_matched_skills(text, job_description)
        missing = find_missing_skills(text, job_description)

        low_signal = is_low_signal(text, skills)

        # LOW SIGNAL MODE
        if low_signal:
            return {
                "detected_skills": skills,
                "final_score": final_score,
                "matched_skills": [],
                "missing_skills": [],
                "suggestions": generate_suggestions(job_description),
                "insight": "Resume lacks clear skills."
            }

        # NORMAL MODE
        return {
            "detected_skills": skills,
            "tfidf_score": tfidf_score,
            "skill_score": skill_score,
            "final_score": final_score,
            "matched_skills": matched,
            "missing_skills": missing,
            "suggestions": generate_suggestions(job_description),
            "insight": generate_insight(matched, missing)
        }

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)