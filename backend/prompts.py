RESUME_ANALYSIS_PROMPT = """
You are an expert ATS Resume Analyzer.

Analyze the following resume against the job description.

RESUME:
{resume}

JOB DESCRIPTION:
{job_description}

Provide:

1. ATS Match Score (0-100)
2. Matching Skills
3. Missing Skills
4. Strengths
5. Weaknesses
6. Suggestions for Improvement
7. Final Recommendation

Format the response clearly using headings.
"""