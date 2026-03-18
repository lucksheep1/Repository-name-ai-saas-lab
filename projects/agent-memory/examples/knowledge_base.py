#!/usr/bin/env python3
"""
Agent Memory - Knowledge Base
==============================
Build a knowledge base with memory.

Usage:
    from knowledge_base import KnowledgeBase
    
    kb = KnowledgeBase()
    kb.add_article("Python", "Python is a programming language.")
    kb.add_article("AI", "AI stands for Artificial Intelligence.")
    results = kb.search("programming")
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Optional
from agent_memory import Memory


class KnowledgeBase:
    """Knowledge base using memory."""
    
    def __init__(self, storage: str = "json", path: str = "./memory.json"):
        self.memory = Memory(storage=storage, path=path)
    
    def add_article(self, title: str, content: str, tags: List[str] = None):
        """Add an article."""
        text = f"{title}: {content}"
        tags = tags or ["article", "kb"]
        
        metadata = {
            "type": "article",
            "title": title,
            "content": content
        }
        
        self.memory.add_with_tags(text, tags=tags, metadata=metadata)
    
    def get_article(self, title: str) -> Optional[Dict]:
        """Get article by title."""
        recent = self.memory.get_recent(limit=self.memory.count())
        
        for mem in recent:
            if mem.get("metadata", {}).get("title") == title:
                return mem
        
        return None
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search knowledge base."""
        return self.memory.search(query, top_k=limit)
    
    def get_all_articles(self) -> List[Dict]:
        """Get all articles."""
        recent = self.memory.get_recent(limit=self.memory.count())
        return [m for m in recent if m.get("metadata", {}).get("type") == "article"]
    
    def delete_article(self, title: str) -> bool:
        """Delete an article."""
        recent = self.memory.get_recent(limit=self.memory.count())
        
        for mem in recent:
            if mem.get("metadata", {}).get("title") == title:
                return self.memory.delete(mem["id"])
        
        return False


# Demo
if __name__ == "__main__":
    import tempfile
    
    demo_path = os.path.join(tempfile.gettempdir(), "kb_demo.json")
    if os.path.exists(demo_path):
        os.remove(demo_path)
    
    print("🤖 Agent Memory - Knowledge Base Demo")
    print("=" * 50)
    
    kb = KnowledgeBase(storage="json", path=demo_path)
    
    # Add articles
    print("\n1. Adding articles...")
    kb.add_article("Python", "Python is a high-level programming language.", ["programming", "language"])
    kb.add_article("Machine Learning", "Machine Learning is a subset of AI.", ["ai", "programming"])
    kb.add_article("Deep Learning", "Deep Learning uses neural networks.", ["ai", "neural-networks"])
    kb.add_article("NLP", "NLP stands for Natural Language Processing.", ["ai", "language"])
    
    print("   Added 4 articles")
    
    # Search
    print("\n2. Searching for 'AI':")
    results = kb.search("AI")
    for r in results:
        title = r.get("metadata", {}).get("title", "")
        content = r.get("metadata", {}).get("content", "")
        print(f"   {title}: {content[:40]}...")
    
    # Get all
    print("\n3. All articles:")
    articles = kb.get_all_articles()
    for a in articles:
        title = a.get("metadata", {}).get("title", "")
        print(f"   - {title}")
    
    print("\n✅ Demo complete!")
    
    if os.path.exists(demo_path):
        os.remove(demo_path)
