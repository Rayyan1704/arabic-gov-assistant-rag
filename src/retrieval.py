import faiss
import numpy as np
import json


class RetrieverSystem:
    def __init__(self, embeddings_path, chunks_path, metadata_path):
        # Load data
        self.embeddings = np.load(embeddings_path).astype('float32')
        
        with open(chunks_path, 'r', encoding='utf-8') as f:
            self.chunks = json.load(f)
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(self.embeddings)
        
        # Build index
        d = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(d)  # Inner product
        self.index.add(self.embeddings)
        
        print(f"✅ Index built with {self.index.ntotal} vectors")
    
    def search(self, query_embedding, k=10):
        """
        Search for k most similar chunks
        """
        # Normalize query
        query_embedding = query_embedding.astype('float32').reshape(1, -1)
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, k)
        
        # Prepare results
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            results.append({
                'rank': i + 1,
                'score': float(score),
                'chunk': self.chunks[idx],
                'metadata': self.metadata[idx]
            })
        
        return results
    
    def save_index(self, path):
        """Save FAISS index to disk"""
        faiss.write_index(self.index, path)
        print(f"✅ Index saved to {path}")
    
    @classmethod
    def load_index(cls, index_path, embeddings_path, chunks_path, metadata_path):
        """Load pre-built index"""
        retriever = cls(embeddings_path, chunks_path, metadata_path)
        retriever.index = faiss.read_index(index_path)
        print(f"✅ Loaded index with {retriever.index.ntotal} vectors")
        return retriever
