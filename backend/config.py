from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # App settings
    app_name: str = "Document AI Platform"
    debug: bool = True
    
    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # File upload
    upload_dir: Path = Path("./uploads")
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_extensions: list = [".pdf", ".docx", ".txt", ".pptx"]
    
    # Database
    database_url: str = "sqlite:///./documents.db"
    
    # NLP
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Embeddings (for later)
    embedding_model: str = "all-MiniLM-L6-v2"
    
    class Config:
        env_file = ".env"

settings = Settings()