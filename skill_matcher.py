def compare_skills(resume_skills, job_skills):

    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched_skills = sorted(
        resume_set.intersection(job_set)
    )

    missing_skills = sorted(
        job_set.difference(resume_set)
    )

    extra_skills = sorted(
        resume_set.difference(job_set)
    )

    if len(job_set) > 0:
        match_percentage = (
            len(matched_skills) / len(job_set)
        ) * 100
    else:
        match_percentage = 0

    return (
        matched_skills,
        missing_skills,
        extra_skills,
        match_percentage
    )