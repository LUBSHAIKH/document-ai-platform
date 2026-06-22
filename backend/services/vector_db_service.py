import chromadb
from typing import List, Dict

class VectorDBService:
    """Manage vector embeddings with Chroma"""
    
    def __init__(self, db_path: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = None
    
    def create_collection(self, document_id: int):
        """Create collection for document"""
        collection_name = f"doc_{document_id}"
        
        # Delete if exists
        try:
            self.client.delete_collection(name=collection_name)
        except:
            pass
        
        self.collection = self.client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        return self.collection
    
    def add_chunks(self, document_id: int, chunks: List[str], embeddings: List[List[float]]):
        """Add text chunks and embeddings to vector DB"""
        collection_name = f"doc_{document_id}"
        collection = self.client.get_collection(name=collection_name)
        
        chunk_ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        collection.add(
            ids=chunk_ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=[{"chunk_index": i} for i in range(len(chunks))]
        )
    
    def search(self, document_id: int, query_embedding: List[float], top_k: int = 3) -> List[Dict]:
        """Search for similar chunks"""
        collection_name = f"doc_{document_id}"
        
        try:
            collection = self.client.get_collection(name=collection_name)
        except:
            return []
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        similar_chunks = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                similar_chunks.append({
                    'text': doc,
                    'distance': results['distances'][0][i] if results['distances'] else 0
                })
        
        return similar_chunks
    
    def delete_collection(self, document_id: int):
        """Delete collection for document"""
        collection_name = f"doc_{document_id}"
        try:
            self.client.delete_collection(name=collection_name)
        except:
            pass