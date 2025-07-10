# gemin model
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-lite")

def generate_questions(text, difficulty):
    prompt = f"Generate 3 study questions from the following text for a {difficulty} level learner:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()
