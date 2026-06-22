from backend.services.embeddings_service import EmbeddingsService
from backend.services.vector_db_service import VectorDBService
from backend.services.llm_service import LLMService
from backend.services.nlp_processor import NLPProcessor
from typing import List, Dict, Generator

class RAGService:
    """Retrieval-Augmented Generation pipeline"""
    
    def __init__(self):
        self.embeddings_service = EmbeddingsService()
        self.vector_db = VectorDBService()
        self.llm = LLMService()
        self.nlp = NLPProcessor()
    
    def index_document(self, document_id: int, text: str):
        """Index a document: create embeddings and store in vector DB"""
        
        print(f"Indexing document {document_id}...")
        
        # 1. Split text into chunks
        chunks = self.nlp.chunk_text(text, chunk_size=500, overlap=100)
        print(f"  Created {len(chunks)} chunks")
        
        # 2. Generate embeddings
        embeddings = self.embeddings_service.generate_embeddings_batch(chunks)
        print(f"  Generated embeddings for {len(embeddings)} chunks")
        
        # 3. Create collection
        self.vector_db.create_collection(document_id)
        
        # 4. Add to vector DB
        self.vector_db.add_chunks(document_id, chunks, embeddings)
        print(f"  ✓ Document {document_id} indexed successfully!")
    
    def retrieve_context(self, document_id: int, query: str, top_k: int = 3) -> str:
        """Retrieve relevant context for a query"""
        
        # 1. Generate embedding for query
        query_embedding = self.embeddings_service.generate_embedding(query)
        
        # 2. Search vector DB
        similar_chunks = self.vector_db.search(document_id, query_embedding, top_k)
        
        # 3. Combine into context
        context = "\n\n".join([chunk['text'] for chunk in similar_chunks])
        return context
    
    def answer_question(self, document_id: int, query: str, top_k: int = 3) -> str:
        """Answer a question about a document (non-streaming)"""
        
        # Retrieve relevant context
        context = self.retrieve_context(document_id, query, top_k)
        
        if not context:
            return "Sorry, I couldn't find relevant information in the document."
        
        # Generate answer
        answer = self.llm.generate_answer(query, context)
        return answer
    
    def answer_question_streaming(self, document_id: int, query: str, top_k: int = 3) -> Generator[str, None, None]:
        """Answer a question with streaming response"""
        
        # Retrieve relevant context
        context = self.retrieve_context(document_id, query, top_k)
        
        if not context:
            yield "Sorry, I couldn't find relevant information in the document."
            return
        
        # Stream answer
        for chunk in self.llm.generate_answer_streaming(query, context):
            yield chunk