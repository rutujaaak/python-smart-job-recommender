import io
import PyPDF2
import re

def extract_resume_text(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_skills_from_resume(text):
    # Basic skill list (you can expand this)
    skill_keywords = [
        "python", "java", "sql", "machine learning", "data analysis",
        "tensorflow", "react", "node.js", "docker", "aws", "html", "css",
        "deep learning", "nlp", "pandas", "numpy", "flask", "django",
        "spark", "hadoop", "excel"
    ]

    text = text.lower()
    found_skills = []

    for skill in skill_keywords:
        if re.search(rf'\b{re.escape(skill)}\b', text):
            found_skills.append(skill)

    return found_skills
