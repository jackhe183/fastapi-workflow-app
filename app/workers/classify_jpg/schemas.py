# app/core/schemas.py
from pydantic import BaseModel
from typing import Dict, Any

class CleanDataRequest(BaseModel):
    source_directory: str
    output_directory: str

class CleanDataResponse(BaseModel):
    status: str
    message: str
    summary: Dict[str, Any]