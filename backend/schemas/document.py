from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class DocumentUploadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    word_count: int
    page_count: Optional[int] = None
    upload_date: datetime
    processed: int

class DocumentDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    raw_text: str
    word_count: int
    page_count: Optional[int] = None
    upload_date: datetime
    processed: int

class DocumentListResponse(BaseModel):
    total: int
    documents: list[DocumentUploadResponse]