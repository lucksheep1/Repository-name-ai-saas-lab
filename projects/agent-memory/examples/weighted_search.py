"""
Memory Weighted Search
Weighted search results
"""
from memory import Memory


class WeightedSearch:
    """Weighted search"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def search(self, query: str, weights: dict = None):
        """Weighted search"""
        weights = weights or {"title": 2, "content": 1, "tags": 3}
        
        results = []
        
        for mem in self.memory.get_all():
            score = 0
            
            content = mem.get("content", "").lower()
            query_lower = query.lower()
            
            # Title match
            if query_lower in content[:50]:
                score += weights.get("title", 1)
            
            # Content match
            if query_lower in content:
                score += weights.get("content", 1)
            
            # Tag match
            for tag in mem.get("tags", []):
                if query_lower in tag.lower():
                    score += weights.get("tags", 1)
            
            if score > 0:
                results.append({**mem, "score": score})
        
        return sorted(results, key=lambda x: x["score"], reverse=True)


def demo():
    """Demo weighted search"""
    memory = Memory(storage="json", path="./weighted_demo.json")
    ws = WeightedSearch(memory)
    
    memory.add("Python tutorial", tags=["python"])
    
    results = ws.search("python")
    print(f"Results: {len(results)}")


if __name__ == "__main__":
    demo()
