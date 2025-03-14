from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from medical_text_summarizer.core.summarizer import Summarizer
import tempfile
import os
import shutil

class SummarizeRequest(BaseModel):
    text: str
    model: str = "gpt-4o-mini"

app = FastAPI(
    title="Medical Text Summarizer API",
    description="API for summarizing medical texts",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Medical Text Summarizer API"}

@app.post("/summarize")
async def summarize_file(
    file: UploadFile = File(...),
    model: str = "gpt-4o-mini"
):
    try:
        # Read the file content
        content = await file.read()
        
        # Create temporary file to store uploaded content
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as temp_file:
            temp_file.write(content)
            input_path = temp_file.name

        # Initialize summarizer and process file
        summarizer = Summarizer(model)
        summary = summarizer.process(input_path, None)  # Remove output_path as it's not needed

        # Clean up temporary file
        os.unlink(input_path)

        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/models")
async def available_models():
    return {
        "models": ["gpt-4o-mini"]  # Add more models as they become available
    }