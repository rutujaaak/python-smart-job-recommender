import os
import requests
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

url = f"https://api.adzuna.com/v1/api/jobs/in/search/1"

params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "results_per_page": 5,
    "what": "Python Developer",
    "where": "India",
    "content-type": "application/json"
}

response = requests.get(url, params=params)

print("Status Code:", response.status_code)
print("Sample Response:")
print(response.json())
