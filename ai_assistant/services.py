import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")


def ai_student_assistant(prompt):

    response = model.generate_content(prompt)
    return response.text
