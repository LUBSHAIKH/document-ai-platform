from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env file from backend directory
env_path = Path(__file__).parent / ".env"  # Changed: removed .parent
if env_path.exists():
    load_dotenv(env_path)
    print(f"✓ Loading .env from: {env_path}")
else:
    print(f"✗ .env file not found at {env_path}")

class Settings(BaseSettings):
    app_name: str = "Document AI Platform"
    debug: bool = True
    
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    upload_dir: Path = Path("./uploads")
    max_file_size: int = 50 * 1024 * 1024
    allowed_extensions: list = [".pdf", ".docx", ".txt", ".pptx"]
    
    database_url: str = "sqlite:///./documents.db"
    
    chunk_size: int = 1000
    chunk_overlap: int = 200
    embedding_model: str = "all-MiniLM-L6-v2"
    
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = "gpt-4o-mini"
    
    vector_db_type: str = "chroma"
    
    class Config:
        env_file = ".env"

settings = Settings()

if settings.openai_api_key:
    print("✓ OpenAI API key loaded successfully")
else:
    print("✗ Warning: OpenAI API key not loaded!")