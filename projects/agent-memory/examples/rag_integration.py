"""
RAG (Retrieval-Augmented Generation) Integration Example
Combines agent-memory with vector search for semantic retrieval
"""
from agent_memory import Memory
import json


class RAGMemory:
    """Memory with semantic search capabilities"""
    
    def __init__(self, storage="sqlite", path="./rag_memory.db"):
        self.memory = Memory(storage=storage, path=path)
        self.threshold = 0.7  # Similarity threshold
    
    def add_context(self, text: str, metadata: dict = None):
        """Add context with metadata"""
        self.memory.add(text, metadata=metadata or {})
    
    def retrieve(self, query: str, top_k: int = 3):
        """Retrieve relevant memories for a query"""
        # Simple keyword-based retrieval (expand with embeddings)
        all_memories = self.memory.get_all()
        
        # Score by keyword overlap
        query_words = set(query.lower().split())
        scored = []
        
        for mem in all_memories:
            content = mem.get("content", "").lower()
            mem_words = set(content.split())
            overlap = len(query_words & mem_words)
            if overlap > 0:
                score = overlap / max(len(query_words), 1)
                scored.append((score, mem))
        
        # Sort by score and return top_k
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored[:top_k]]
    
    def generate_context(self, query: str) -> str:
        """Generate context string for LLM prompt"""
        relevant = self.retrieve(query, top_k=5)
        
        if not relevant:
            return "No relevant history found."
        
        context = "## Relevant Context:\n"
        for i, mem in enumerate(relevant, 1):
            context += f"\n{i}. {mem.get('content', '')}"
            if mem.get("metadata"):
                context += f" (meta: {mem['metadata']})"
        
        return context


def demo():
    """Demo RAG memory usage"""
    rag = RAGMemory(storage="json", path="./rag_demo.json")
    
    # Add various contexts
    rag.add_context(
        "User prefers dark mode in the UI",
        {"source": "settings", "priority": "high"}
    )
    rag.add_context(
        "Python 3.10+ is required for this project",
        {"source": "docs", "priority": "medium"}
    )
    rag.add_context(
        "The API endpoint is https://api.example.com/v1",
        {"source": "config", "priority": "high"}
    )
    rag.add_context(
        "User wants to export data as CSV format",
        {"source": "request", "priority": "medium"}
    )
    
    # Query relevant context
    queries = [
        "How should I display the UI?",
        "What's the API URL?",
        "What format should I export?",
    ]
    
    print("=== RAG Memory Demo ===\n")
    for q in queries:
        print(f"Query: {q}")
        context = rag.generate_context(q)
        print(f"Context: {context}\n")


if __name__ == "__main__":
    demo()
