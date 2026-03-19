"""
Memory Search Suggestions
Auto-complete and suggestions for search
"""
from agent_memory import Memory
from collections import Counter


class SearchSuggester:
    """Generate search suggestions"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.history = Counter()
    
    def suggest(self, prefix: str, limit: int = 5) -> list:
        """Suggest based on prefix"""
        suggestions = []
        
        # From content
        for mem in self.memory.get_all():
            words = mem.get("content", "").lower().split()
            for word in words:
                if word.startswith(prefix.lower()):
                    suggestions.append(word)
        
        # From tags
        for mem in self.memory.get_all():
            for tag in mem.get("tags", []):
                if tag.startswith(prefix.lower()):
                    suggestions.append(tag)
        
        # From search history
        for query, count in self.history.most_common():
            if query.startswith(prefix.lower()):
                suggestions.append(query)
        
        # Return top results
        return list(set(suggestions))[:limit]
    
    def record_search(self, query: str):
        """Record search for suggestions"""
        self.history[query.lower()] += 1
    
    def popular(self, limit: int = 10) -> list:
        """Get popular searches"""
        return [q for q, _ in self.history.most_common(limit)]


def demo():
    """Demo suggestions"""
    memory = Memory(storage="json", path="./suggest_demo.json")
    suggester = SearchSuggester(memory)
    
    print("=== Search Suggester Demo ===\n")
    
    # Add memories
    memory.add("Python tutorial", tags=["python", "tutorial"])
    memory.add("JavaScript guide", tags=["javascript", "guide"])
    memory.add("Python tips", tags=["python", "tips"])
    memory.add("Machine learning", tags=["ml", "ai"])
    
    # Suggest
    print("Suggestions for 'py':")
    for s in suggester.suggest("py"):
        print(f"  {s}")
    
    print("\nSuggestions for 'java':")
    for s in suggester.suggest("java"):
        print(f"  {s}")
    
    # Record searches
    suggester.record_search("python")
    suggester.record_search("python")
    suggester.record_search("python tips")
    
    print("\nPopular searches:")
    for s in suggester.popular():
        print(f"  {s}")
    
    # Cleanup
    import os
    if os.path.exists("./suggest_demo.json"):
        os.remove("./suggest_demo.json")


if __name__ == "__main__":
    demo()
