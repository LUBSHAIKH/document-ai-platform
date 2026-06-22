from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingsService:
    """Generate embeddings for text using sentence-transformers"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding.tolist()
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return [emb.tolist() for emb in embeddings]
    
    def similarity_score(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts (0-1)"""
        emb1 = self.model.encode(text1, convert_to_tensor=True)
        emb2 = self.model.encode(text2, convert_to_tensor=True)
        
        from sentence_transformers.util import pytorch_cos_sim
        similarity = pytorch_cos_sim(emb1, emb2)
        return float(similarity[0][0])