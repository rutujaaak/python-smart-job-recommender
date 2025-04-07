import streamlit as st
import requests
from resume_parser import extract_resume_text, extract_skills_from_resume
from dotenv import load_dotenv
import os

# Set page config
st.set_page_config(page_title="Smart Job Recommender", layout="centered")

# Load environment variables (if needed)
load_dotenv()

ADZUNA_APP_ID = "9f889da2"
ADZUNA_APP_KEY = "72dbed2d8a0d69632bf9fa4fa632c3f7"

# ---------------------------
# Fetch Real-time Jobs (Adzuna API)
# ---------------------------
def fetch_adzuna_jobs(keyword="Python Developer", location="India"):
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"
    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 10,
        "what": keyword,
        "where": location,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        st.error(f"❌ Failed to fetch jobs. Status Code: {response.status_code}")
        st.code(response.text)
        return []

# ---------------------------
# Fetch Company Posts (LinkedIn API)
# ---------------------------
def get_company_posts(username="microsoft", start=0):
    url = "https://linkedin-data-api.p.rapidapi.com/get-company-posts"
    headers = {
        "x-rapidapi-key": "689956bdbamsh317a7a9049337f8p1707afjsn5e688b6e010a",  # Keep or update if needed
        "x-rapidapi-host": "linkedin-data-api.p.rapidapi.com"
    }
    querystring = {"username": username, "start": str(start)}

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        return []

# ---------------------------
# Custom CSS: Gradient Background
# ---------------------------
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #223843, #3e5673, #f0f4f8);
            background-attachment: fixed;
            color: white;
        }
        header, footer, .css-1rs6os.edgvbvh3 {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h2 style='text-align: center;'>Smart Job Recommender 🔍</h2>", unsafe_allow_html=True)

# ---------------------------
# Upload Resume & Recommend Jobs
# ---------------------------
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    resume_text = extract_resume_text(uploaded_file)
    skills = extract_skills_from_resume(resume_text)

    if skills:
        top_skill = skills[0]
        st.success(f"Top skill from resume: **{top_skill}**")

        jobs = fetch_adzuna_jobs(keyword=top_skill)

        if jobs:
            st.subheader("🔗 Real-Time Job Recommendations")
            for job in jobs:
                st.markdown(f"### {job.get('title', 'No Title')}")
                st.write(f"📍 {job.get('location', {}).get('display_name', 'Unknown')}")
                st.write(f"🏢 {job.get('company', {}).get('display_name', 'Unknown')}")
                st.write(f"📝 {job.get('description', '')[:250]}...")

                apply_link = job.get("redirect_url")
                if apply_link:
                    st.markdown(f"[Apply Here]({apply_link})")
                else:
                    st.info("No application link available.")

                st.markdown("---")
        else:
            st.warning("No jobs found for this skill.")
    else:
        st.warning("Couldn’t extract skills from resume.")

# ---------------------------
# Company Posts Section
# ---------------------------
st.subheader("📢 Latest Company Posts")

company = st.text_input("Enter LinkedIn company username (e.g., microsoft):")

if company:
    posts = get_company_posts(username=company)

    if posts:
        for post in posts:
            st.markdown(f"#### {post.get('title', 'No Title')}")
            st.write(post.get("content", "No content available"))
            st.markdown("---")
    else:
        st.warning("No posts found or invalid username.")

# ---------------------------
# Footer
# ---------------------------
st.markdown("<div style='text-align: center; margin-top: 50px;'>Made with ❤️ by Rutuja Kale</div>", unsafe_allow_html=True)
