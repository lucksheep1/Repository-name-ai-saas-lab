"""
Memory Fuzzy Search
Search with typos and approximate matching
"""
from agent_memory import Memory
import re


class FuzzySearch:
    """Fuzzy search for memories"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def search(self, query: str, threshold: float = 0.6) -> list:
        """Fuzzy search"""
        query_words = query.lower().split()
        results = []
        
        for mem in self.memory.get_all():
            content = mem.get("content", "").lower()
            content_words = content.split()
            
            # Calculate similarity
            score = self._fuzzy_score(query_words, content_words)
            
            if score >= threshold:
                results.append({**mem, "fuzzy_score": score})
        
        # Sort by score
        results.sort(key=lambda m: m.get("fuzzy_score", 0), reverse=True)
        return results
    
    def _fuzzy_score(self, query_words: list, content_words: list) -> float:
        """Calculate fuzzy match score"""
        if not query_words or not content_words:
            return 0.0
        
        matches = 0
        for qw in query_words:
            # Check exact match
            if qw in content_words:
                matches += 1
                continue
            
            # Check substring match
            for cw in content_words:
                if qw in cw or cw in qw:
                    matches += 0.8
                    break
        
        return matches / len(query_words)


class SmartSearch:
    """Smart search with operators"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def search(self, query: str) -> list:
        """Search with operators
        
        Operators:
          tag:bug - search by tag
          priority:5 - search by priority
          "exact phrase" - exact match
          -exclude - exclude term
        """
        results = self.memory.get_all()
        
        # Tag filter
        if "tag:" in query:
            match = re.search(r"tag:(\w+)", query)
            if match:
                tag = match.group(1)
                results = [m for m in results if tag in m.get("tags", [])]
                query = query.replace(f"tag:{tag}", "")
        
        # Priority filter
        if "priority:" in query:
            match = re.search(r"priority:(\d+)", query)
            if match:
                priority = int(match.group(1))
                results = [m for m in results 
                          if m.get("metadata", {}).get("priority") == priority]
                query = query.replace(f"priority:{priority}", "")
        
        # Exclude
        if "-" in query:
            parts = query.split("-")
            main_query = parts[0].strip()
            exclude = parts[1].strip()
            
            results = [m for m in results if exclude not in m.get("content", "").lower()]
            query = main_query
        
        # Text search
        if query.strip():
            query_lower = query.lower()
            results = [m for m in results 
                      if query_lower in m.get("content", "").lower()]
        
        return results


def demo():
    """Demo fuzzy search"""
    memory = Memory(storage="json", path="./fuzzy_demo.json")
    fuzzy = FuzzySearch(memory)
    smart = SmartSearch(memory)
    
    print("=== Fuzzy Search Demo ===\n")
    
    # Add memories
    memory.add("Python programming tips")
    memory.add("JavaScript tutorial")
    memory.add("Python is great for AI")
    memory.add("Javascript vs Python")
    
    # Fuzzy search
    print("Fuzzy search 'pyton' (typo):")
    results = fuzzy.search("pyton")
    for r in results:
        print(f"  [{r.get('fuzzy_score'):.2f}] {r.get('content')}")
    
    print("\nSmart search 'tag:bug':")
    # Add tagged
    memory.add("Bug in code", tags=["bug"])
    results = smart.search("tag:bug")
    for r in results:
        print(f"  {r.get('content')}")
    
    # Cleanup
    import os
    if os.path.exists("./fuzzy_demo.json"):
        os.remove("./fuzzy_demo.json")


if __name__ == "__main__":
    demo()
