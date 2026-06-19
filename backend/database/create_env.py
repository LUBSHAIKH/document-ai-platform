# backend/create_env.py
env_content = """DEBUG=True
UPLOAD_DIR=./uploads
DATABASE_URL=sqlite:///./documents.db
EMBEDDING_MODEL=all-MiniLM-L6-v2
"""

with open('.env', 'w') as f:
    f.write(env_content)

print(".env file created successfully!")