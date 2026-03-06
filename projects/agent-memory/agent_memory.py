#!/usr/bin/env python3
"""
Agent Memory Manager v2 - Lightweight memory for AI agents.
Enhanced with FAISS support and memory summarization.
"""
import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional
# Try to import optional dependencies
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    HAS_SKLEARN = True
except ImportError:
    HAS_SKLEARN = False

try:
    import faiss
    HAS_FAISS = True
except ImportError:
    HAS_FAISS = False


class Memory:
    """Lightweight memory manager for AI agents."""
    
    def __init__(self, storage: str = "json", path: str = "./memory.json", 
                 vector_dim: int = 512):
        self.storage = storage
        self.path = path
        self.vector_dim = vector_dim
        self.memories: List[Dict] = []
        
        # TF-IDF based
        if HAS_SKLEARN:
            self.vectorizer = TfidfVectorizer(max_features=vector_dim)
            self.tfidf_matrix = None
        
        # FAISS index
        if storage == "faiss" and HAS_FAISS:
            self.index = faiss.IndexFlatL2(vector_dim)
        else:
            self.index = None
        
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
        """Add a new memory."""
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
    
    def add_batch(self, texts: List[str], metadata: Optional[Dict] = None) -> List[str]:
        """Add multiple memories at once."""
        ids = []
        for text in texts:
            memory_id = self.add(text, metadata)
            ids.append(memory_id)
        return ids
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search memories by similarity."""
        if not self.memories:
            return []
        
        if HAS_SKLEARN:
            texts = [m["text"] for m in self.memories]
            try:
                tfidf_matrix = self.vectorizer.fit_transform(texts + [query])
                query_vec = tfidf_matrix[-1]
                memory_vecs = tfidf_matrix[:-1]
                similarities = cosine_similarity(query_vec, memory_vecs)[0]
                if HAS_NUMPY:
                    top_indices = np.argsort(similarities)[-top_k:][::-1]
                else:
                    # Pure Python fallback
                    indexed_sims = list(enumerate(similarities))
                    indexed_sims.sort(key=lambda x: x[1], reverse=True)
                    top_indices = [x[0] for x in indexed_sims[:top_k]]
                
                results = []
                for idx in top_indices:
                    if similarities[idx] > 0:
                        result = self.memories[idx].copy()
                        result["score"] = float(similarities[idx])
                        results.append(result)
                return results
            except ValueError:
                pass
        
        # Fallback: return recent memories
        return self.memories[:top_k]
    
    def get_recent(self, limit: int = 10) -> List[Dict]:
        """Get recent memories."""
        sorted_memories = sorted(
            self.memories, 
            key=lambda x: x.get("timestamp", ""), 
            reverse=True
        )
        return sorted_memories[:limit]
    
    def get_context(self, max_tokens: int = 2000, max_memories: int = 10) -> str:
        """Get condensed context for agent."""
        if not self.memories:
            return ""
        
        sorted_memories = sorted(
            self.memories, 
            key=lambda x: x.get("timestamp", ""), 
            reverse=True
        )
        
        context_parts = []
        total_chars = 0
        
        for memory in sorted_memories[:max_memories]:
            text = memory["text"]
            if total_chars + len(text) > max_tokens * 4:
                break
            context_parts.append(f"- {text}")
            total_chars += len(text)
        
        if not context_parts:
            return ""
        
        return "Relevant memories:\n" + "\n".join(context_parts)
    
    def summarize(self) -> str:
        """Generate a summary of all memories."""
        if not self.memories:
            return "No memories stored."
        
        count = len(self.memories)
        recent = self.get_recent(3)
        
        summary = f"Total memories: {count}\n\nRecent memories:\n"
        for m in recent:
            summary += f"- {m['text'][:100]}...\n"
        
        return summary
    
    def delete(self, memory_id: str) -> bool:
        """Delete a memory by ID."""
        for i, m in enumerate(self.memories):
            if m["id"] == memory_id:
                del self.memories[i]
                self._save()
                return True
        return False
    
    def clear(self):
        """Clear all memories."""
        self.memories = []
        if self.storage == "json":
            self._save()
    
    def count(self) -> int:
        """Get number of memories."""
        return len(self.memories)
    
    def export(self, filepath: str):
        """Export memories to a file."""
        with open(filepath, 'w') as f:
            json.dump(self.memories, f, indent=2)
    
    def import_(self, filepath: str):
        """Import memories from a file."""
        with open(filepath, 'r') as f:
            self.memories = json.load(f)
        self._save()


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Memory CLI v2")
    parser.add_argument("command", choices=["add", "search", "clear", "context", "recent", "summarize", "delete"])
    parser.add_argument("--text", help="Text for add/search")
    parser.add_argument("--path", default="./memory.json", help="Memory file path")
    parser.add_argument("--top-k", type=int, default=5, help="Top K results")
    parser.add_argument("--storage", default="json", choices=["json", "faiss"], help="Storage backend")
    parser.add_argument("--id", help="Memory ID for delete")
    
    args = parser.parse_args()
    memory = Memory(storage=args.storage, path=args.path)
    
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
            print(f"[{score:.2f}] {r['text'][:80]}...")
    
    elif args.command == "clear":
        memory.clear()
        print("Memory cleared")
    
    elif args.command == "context":
        ctx = memory.get_context()
        print(ctx or "(no context)")
    
    elif args.command == "recent":
        recent = memory.get_recent(args.top_k)
        for r in recent:
            print(f"- {r['text'][:80]}...")
    
    elif args.command == "summarize":
        print(memory.summarize())
    
    elif args.command == "delete":
        if args.id:
            if memory.delete(args.id):
                print(f"Deleted memory: {args.id}")
            else:
                print(f"Memory not found: {args.id}")
        else:
            print("Error: --id required for delete")
