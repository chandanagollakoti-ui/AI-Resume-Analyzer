from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pdf_reader import extract_text_from_pdf
from gemini_service import analyze_resume

import os

app = FastAPI(
    title="AI Resume Analyzer",
    version="1.0"
)

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

@app.get("/")
def home():
    return {
        "message": "AI Resume Analyzer API"
    }

@app.get("/health")
def health():
    return {
        "status": "running"
    }

@app.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    try:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(file_path, "wb") as f:
            f.write(await file.read())

        resume_text = extract_text_from_pdf(
            file_path
        )

        analysis = analyze_resume(
            resume_text,
            job_description
        )

        return {
            "filename": file.filename,
            "analysis": analysis
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )