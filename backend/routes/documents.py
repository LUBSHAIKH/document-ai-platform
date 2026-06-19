from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.config import settings
from backend.models.document import Document
from backend.schemas.document import DocumentUploadResponse, DocumentDetail, DocumentListResponse
from backend.services.document_processor import DocumentProcessor
from backend.services.nlp_processor import NLPProcessor
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/documents", tags=["documents"])

# Initialize services
doc_processor = DocumentProcessor(settings.upload_dir)
nlp_processor = NLPProcessor()

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a document and extract text"""
    
    # Validate file type
    file_ext = "." + file.filename.split(".")[-1].lower()
    if file_ext not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not supported. Allowed: {settings.allowed_extensions}"
        )
    
    # Validate file size
    file_content = await file.read()
    if len(file_content) > settings.max_file_size:
        raise HTTPException(
            status_code=413,
            detail=f"File size exceeds maximum of {settings.max_file_size / (1024*1024):.1f}MB"
        )
    
    # Reset file pointer
    await file.seek(0)
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    
    try:
        # Save file
        file_path = doc_processor.save_uploaded_file(file, unique_filename)
        
        # Extract text
        raw_text, page_count = doc_processor.extract_text(file_path, file_ext)
        
        # Clean text
        raw_text = doc_processor.clean_text(raw_text)
        
        # Calculate word count
        word_count = doc_processor.get_word_count(raw_text)
        
        # Create database record
        db_document = Document(
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_type=file_ext.lstrip("."),
            file_size=len(file_content),
            raw_text=raw_text,
            word_count=word_count,
            page_count=page_count,
            upload_date=datetime.utcnow(),
            processed=0
        )
        
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        return db_document
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=DocumentListResponse)
async def list_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get list of uploaded documents"""
    
    total = db.query(Document).count()
    documents = db.query(Document).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "documents": documents
    }

@router.get("/{doc_id}", response_model=DocumentDetail)
async def get_document(doc_id: int, db: Session = Depends(get_db)):
    """Get document details"""
    
    document = db.query(Document).filter(Document.id == doc_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document

@router.get("/{doc_id}/analyze", response_model=dict)
async def analyze_document(doc_id: int, db: Session = Depends(get_db)):
    """Analyze document and extract insights"""
    
    document = db.query(Document).filter(Document.id == doc_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not document.raw_text:
        raise HTTPException(status_code=400, detail="Document has no text content")
    
    try:
        # Extract sentences
        sentences = nlp_processor.tokenize_sentences(document.raw_text)
        
        # Extract entities
        entities = nlp_processor.extract_entities(document.raw_text)
        
        # Extract key phrases
        key_phrases = nlp_processor.extract_key_phrases(document.raw_text)
        
        # Create chunks for later RAG
        chunks = nlp_processor.chunk_text(document.raw_text)
        
        return {
            "document_id": doc_id,
            "filename": document.original_filename,
            "word_count": document.word_count,
            "sentence_count": len(sentences),
            "entities": entities,
            "key_phrases": key_phrases,
            "chunk_count": len(chunks),
            "analysis_timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{doc_id}")
async def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """Delete a document"""
    
    document = db.query(Document).filter(Document.id == doc_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete file
    import os
    try:
        os.remove(document.file_path)
    except:
        pass
    
    # Delete from database
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}