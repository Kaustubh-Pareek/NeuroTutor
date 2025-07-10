# gemin model
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-lite")


def generate_concepts(summary, difficulty):
    try:
        prompt = f"From the following summary, extract the 5 most important key concepts as a bullet list:\n\n{summary} for a {difficulty} level learner."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception: #can be rate limit or network issue etc.
        return "\n".join(
            line for line in summary.splitlines()
            if len(line) > 40 and ('•' in line or '-' in line or ':' in line)
        )

