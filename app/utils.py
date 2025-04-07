
def match_resume_to_jobs(resume_skills, job_df):
    matched_jobs = []

    for _, row in job_df.iterrows():
        job_description = row.get("description", "").lower()
        for skill in resume_skills:
            if skill in job_description:
                matched_jobs.append(row)
                break

    return matched_jobs
