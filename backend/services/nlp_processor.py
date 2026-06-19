import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

class NLPProcessor:
    """Handles NLP operations on documents"""
    
    def __init__(self):
        pass
    
    @staticmethod
    def tokenize_sentences(text: str) -> list[str]:
        """Split text into sentences"""
        try:
            sentences = sent_tokenize(text)
            return [s.strip() for s in sentences if s.strip()]
        except:
            return text.split(". ")
    
    @staticmethod
    def tokenize_words(text: str) -> list[str]:
        """Tokenize text into words"""
        try:
            tokens = word_tokenize(text.lower())
            return tokens
        except:
            return text.lower().split()
    
    @staticmethod
    def remove_stopwords(tokens: list[str]) -> list[str]:
        """Remove common stopwords"""
        try:
            stop_words = set(stopwords.words('english'))
            return [token for token in tokens if token.isalnum() and token not in stop_words]
        except:
            return tokens
    
    @staticmethod
    def extract_key_phrases(text: str, num_phrases: int = 10) -> list[str]:
        """Extract important words"""
        try:
            tokens = word_tokenize(text.lower())
            clean_tokens = [t for t in tokens if t.isalnum()]
            
            stop_words = set(stopwords.words('english'))
            filtered = [t for t in clean_tokens if t not in stop_words and len(t) > 3]
            
            counter = Counter(filtered)
            return [word for word, _ in counter.most_common(num_phrases)]
        except:
            return []
    
    def extract_entities(self, text: str) -> list[dict]:
        """Basic entity extraction"""
        return []
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start = end - overlap
        
        return chunks