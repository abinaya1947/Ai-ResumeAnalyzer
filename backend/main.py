from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("gemini-3.5-flash")

# Create FastAPI app
app = FastAPI(
    title="AI Resume Analyzer API",
    version="1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home Route
@app.get("/")
def home():
    return {
        "message": "AI Resume Analyzer API is running successfully!"
    }

# Analyze Resume Route
@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_role: str = Form(...)
):
    # Read uploaded resume
    resume_text = (await resume.read()).decode("utf-8", errors="ignore")

    prompt = f"""
You are an ATS Resume Analyzer.

Analyze the following resume for the role of {job_role}.

Provide:

1. Resume Score out of 100
2. Strengths
3. Weaknesses
4. Missing Skills
5. Suggestions to Improve
6. 5 Interview Questions

Resume:
{resume_text}
"""

    response = model.generate_content(prompt)

    return {
        "analysis": response.text
    }