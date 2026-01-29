from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from analyzer import analyze_resume, extract_text_from_pdf
import os
import tempfile

app = FastAPI(title="Resume Analyzer API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"message": "Resume Analyzer API is running"}

@app.post("/analyze")
async def analyze(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    if not resume_file or not job_description:
        raise HTTPException(status_code=400, detail="Both resume file and job description are required.")
    
    if not resume_file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for resume upload.")

    try:
        # Create a temporary file to save the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await resume_file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # Extract text from the temporary PDF
        resume_text = extract_text_from_pdf(tmp_path)
        
        # Clean up the temporary file
        os.unlink(tmp_path)

        if not resume_text or len(resume_text) < 10:
            raise HTTPException(
                status_code=400, 
                detail="Could not extract enough text from the PDF. Please ensure it is a searchable PDF and not just a scanned image."
            )

        results = analyze_resume(resume_text, job_description)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
