# from transformers import pipeline

# generator = pipeline("text-generation", model="google/flan-t5-base")

# def generate_answer(prompt):
#     result = generator(prompt, max_length=300, do_sample=True)
#     print(result,"Generated result")
#     return result[0]["generated_text"]

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model_gemini = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

def generate_answer(prompt):
    try:
        print("Prompt sent to Gemini:\n", prompt)
        response = model_gemini.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Error occurred while generating answer:", e)
    