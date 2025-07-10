# gemin model
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-lite")

def summarize(text, difficulty):
    prompt = f"Summarize this text for a {difficulty} level student:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text.strip()
