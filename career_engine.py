from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from skill_matcher import compare_skills
from career_recommender import get_recommendations


def analyze_career(resume_text, job_description):

    # Extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    # Compare skills
    (
        matched_skills,
        missing_skills,
        extra_skills,
        match_percentage
    ) = compare_skills(
        resume_skills,
        job_skills
    )

    # Generate recommendations
    recommendations = get_recommendations(
        missing_skills
    )

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
        "match_percentage": match_percentage,
        "recommendations": recommendations
    }