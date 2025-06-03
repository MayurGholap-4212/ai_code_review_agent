from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import tempfile
import shutil
import sys
import os

# 🔧 Add project root (ai_code_review_agent/) to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import ReviewRequest, ReviewResponse
from analyzer.improve import improve_codebase
from analyzer.analyze import analyze_codebase

app = FastAPI(
    title="AI Code Review API",
    description="REST API for programmatic code review",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import FileResponse
from fastapi import Request

@app.get("/download/{filename}")
async def download_file(filename: str):
    download_path = Path(r"E:\assignment\ai_code_review_agent\output") / filename  # adjust this path
    if download_path.exists():
        return FileResponse(path=download_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import Optional
import json

@app.post("/review")
async def review_code(
    source_path: Optional[str] = Form(None),
    zip_file: Optional[UploadFile] = File(None),
    languages: str = Form('["py"]'),
    priority: str = Form("readability")
):
    try:
        # Parse languages from string to list
        languages_list = json.loads(languages)
        
        if not source_path and not zip_file:
            raise HTTPException(status_code=400, detail="Either source_path or zip_file must be provided")
        
        # Process the request
        result = improve_codebase(
            source_path=source_path,
            zip_file=zip_file,
            languages=languages_list,
            priority=priority
        )
        
        return result
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid languages format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))