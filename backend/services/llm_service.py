from openai import OpenAI
from typing import List, Generator
from backend.config import settings

class LLMService:
    """Interact with OpenAI GPT models"""
    
    def __init__(self, api_key: str = None):
        self.client = OpenAI(api_key=api_key or settings.openai_api_key)
        self.model = settings.openai_model
    
    def generate_answer(self, query: str, context: str) -> str:
        """Generate answer based on query and context"""
        
        system_prompt = """You are a helpful AI assistant that answers questions based on 
provided document context. Be concise, accurate, and cite the context when possible.
If the answer is not in the context, say so clearly."""
        
        user_message = f"""Context from document:
{context}

Question: {query}

Please provide a clear, concise answer based on the context provided."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=500,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        
        return response.choices[0].message.content
    
    def generate_answer_streaming(self, query: str, context: str) -> Generator[str, None, None]:
        """Generate answer with streaming"""
        
        system_prompt = """You are a helpful AI assistant that answers questions based on 
provided document context. Be concise, accurate, and cite the context when possible."""
        
        user_message = f"""Context from document:
{context}

Question: {query}

Please provide a clear, concise answer based on the context provided."""
        
        with self.client.chat.completions.create(
            model=self.model,
            max_tokens=500,
            stream=True,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        ) as stream:
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
    
    def summarize_text(self, text: str) -> str:
        """Summarize a text"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=200,
            messages=[
                {"role": "user", "content": f"Summarize this text concisely:\n\n{text}"}
            ]
        )
        
        return response.choices[0].message.content