"""
Agent Memory Manager - Lightweight memory for AI agents.
"""
import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Memory:
    """Lightweight memory manager for AI agents."""
    
    def __init__(self, storage: str = "json", path: str = "./memory.json"):
        self.storage = storage
        self.path = path
        self.memories: List[Dict] = []
        self.vectorizer = TfidfVectorizer(max_features=512)
        
        if storage == "json" and os.path.exists(path):
            self._load()
    
    def _load(self):
        """Load memories from file."""
        with open(self.path, 'r') as f:
            self.memories = json.load(f)
    
    def _save(self):
        """Save memories to file."""
        with open(self.path, 'w') as f:
            json.dump(self.memories, f, indent=2)
    
    def add(self, text: str, metadata: Optional[Dict] = None) -> str:
        """
        Add a new memory.
        
        Args:
            text: The memory content
            metadata: Optional metadata (source, timestamp, etc.)
        
        Returns:
            Memory ID
        """
        memory_id = str(uuid.uuid4())[:8]
        memory = {
            "id": memory_id,
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.memories.append(memory)
        self._save()
        return memory_id
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search memories by similarity.
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            List of relevant memories
        """
        if not self.memories:
            return []
        
        # Get all memory texts
        texts = [m["text"] for m in self.memories]
        
        # Fit vectorizer and transform
        try:
            tfidf_matrix = self.vectorizer.fit_transform(texts + [query])
            query_vec = tfidf_matrix[-1]
            memory_vecs = tfidf_matrix[:-1]
        except ValueError:
            # Not enough vocabulary
            return self.memories[:top_k]
        
        # Calculate similarities
        similarities = cosine_similarity(query_vec, memory_vecs)[0]
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:
                result = self.memories[idx].copy()
                result["score"] = float(similarities[idx])
                results.append(result)
        
        return results
    
    def get_context(self, max_tokens: int = 2000, max_memories: int = 10) -> str:
        """
        Get condensed context for agent.
        
        Args:
            max_tokens: Target token count (approximate)
            max_memories: Maximum memories to include
        
        Returns:
            Context string
        """
        if not self.memories:
            return ""
        
        # Get recent memories (sorted by timestamp)
        sorted_memories = sorted(
            self.memories, 
            key=lambda x: x.get("timestamp", ""), 
            reverse=True
        )
        
        context_parts = []
        total_chars = 0
        
        for memory in sorted_memories[:max_memories]:
            text = memory["text"]
            if total_chars + len(text) > max_tokens * 4:  # Rough token estimate
                break
            context_parts.append(f"- {text}")
            total_chars += len(text)
        
        if not context_parts:
            return ""
        
        return "Relevant memories:\n" + "\n".join(context_parts)
    
    def clear(self):
        """Clear all memories."""
        self.memories = []
        if self.storage == "json":
            self._save()
    
    def count(self) -> int:
        """Get number of memories."""
        return len(self.memories)


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Memory CLI")
    parser.add_argument("command", choices=["add", "search", "clear", "context"])
    parser.add_argument("--text", help="Text for add/search")
    parser.add_argument("--path", default="./memory.json", help="Memory file path")
    parser.add_argument("--top-k", type=int, default=5, help="Top K results")
    
    args = parser.parse_args()
    memory = Memory(path=args.path)
    
    if args.command == "add":
        if not args.text:
            print("Error: --text required for add")
            exit(1)
        memory_id = memory.add(args.text)
        print(f"Added memory: {memory_id}")
    
    elif args.command == "search":
        if not args.text:
            print("Error: --text required for search")
            exit(1)
        results = memory.search(args.text, args.top_k)
        for r in results:
            score = r.get("score", 0)
            print(f"[{score:.2f}] {r['text']}")
    
    elif args.command == "clear":
        memory.clear()
        print("Memory cleared")
    
    elif args.command == "context":
        ctx = memory.get_context()
        print(ctx or "(no context)")
