from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.5-flash")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_role: str = Form(...)
):
    resume_text = (await resume.read()).decode("utf-8", errors="ignore")

    prompt = f"""
You are an ATS Resume Analyzer.

Analyze this resume for the role: {job_role}

Provide:

1. Resume Score /100
2. Strengths
3. Weaknesses
4. Missing Skills
5. Improvement Suggestions
6. 5 Interview Questions

Resume:

{resume_text}
"""

    response = model.generate_content(prompt)

    return {
        "analysis": response.text
    }