"""
Memory FTS (Full-Text Search) Demo
Full-text search capabilities
"""
from agent_memory import Memory
import re


class FTSMemory:
    """Full-text search for memory"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def search_advanced(self, query: str, options: dict = None) -> list:
        """Advanced search with options"""
        options = options or {}
        
        results = []
        
        for mem in self.memory.get_all():
            content = mem.get("content", "").lower()
            query_lower = query.lower()
            
            # Simple FTS: word matching
            matches = []
            
            # AND search
            if options.get("AND"):
                words = query_lower.split()
                if all(w in content for w in words):
                    matches.append("AND")
            
            # OR search
            if options.get("OR"):
                words = query_lower.split()
                if any(w in content for w in words):
                    matches.append("OR")
            
            # Phrase search
            if options.get("phrase"):
                if query_lower in content:
                    matches.append("PHRASE")
            
            # Regex search
            if options.get("regex"):
                try:
                    if re.search(options["regex"], content, re.I):
                        matches.append("REGEX")
                except:
                    pass
            
            # Default: simple contains
            if not matches:
                if query_lower in content:
                    matches.append("CONTAINS")
            
            if matches:
                results.append({**mem, "match_type": matches[0]})
        
        return results
    
    def highlight(self, query: str) -> list:
        """Highlight matching terms"""
        results = []
        
        for mem in self.memory.get_all():
            content = mem.get("content", "")
            
            # Highlight
            pattern = re.compile(re.escape(query), re.I)
            highlighted = pattern.sub(f"**{query}**", content)
            
            results.append({
                **mem,
                "highlighted": highlighted
            })
        
        return results


def demo():
    """Demo FTS"""
    memory = Memory(storage="json", path="./fts_demo.json")
    fts = FTSMemory(memory)
    
    print("=== FTS Demo ===\n")
    
    # Add memories
    memory.add("Python is great for AI")
    memory.add("JavaScript is great for web")
    memory.add("Python and JavaScript are both popular")
    memory.add("I love programming in Python")
    
    # Basic search
    results = fts.search_advanced("Python")
    print(f"Basic search 'Python': {len(results)} results")
    
    # AND search
    results = fts.search_advanced("Python", {"AND": True})
    print(f"AND search 'Python': {len(results)} results")
    
    # Highlight
    results = fts.highlight("Python")
    print("\nHighlight results:")
    for r in results[:2]:
        print(f"  {r.get('highlighted')}")
    
    # Cleanup
    import os
    if os.path.exists("./fts_demo.json"):
        os.remove("./fts_demo.json")


if __name__ == "__main__":
    demo()
