from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    original_filename = Column(String)
    file_path = Column(String)
    file_type = Column(String)
    file_size = Column(Integer)
    
    raw_text = Column(Text)
    word_count = Column(Integer)
    page_count = Column(Integer, nullable=True)
    
    # Week 2: New fields
    indexed = Column(Boolean, default=False)
    indexed_at = Column(DateTime, nullable=True)
    embedding_chunks = Column(Integer, default=0)
    
    upload_date = Column(DateTime, default=datetime.utcnow, index=True)
    processed = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<Document {self.filename}>"