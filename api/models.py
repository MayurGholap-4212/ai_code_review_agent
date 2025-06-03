from pydantic import BaseModel
from typing import List, Optional, Union
from enum import Enum
from fastapi import UploadFile

class Priority(str, Enum):
    security = "security"
    performance = "performance"
    readability = "readability"

class ReviewRequest(BaseModel):
    source_path: Optional[str] = None
    zip_file: Optional[UploadFile] = None
    languages: List[str] = ['py']
    priority: Priority = Priority.readability
    exclude: List[str] = []

class ReviewResponse(BaseModel):
    improvements: List[dict]
    metrics: dict
    download_url: str