"""
Memory Analytics
Analytics and insights
"""
from agent_memory import Memory
from collections import Counter


class MemoryAnalytics:
    """Analytics for memory"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def get_stats(self) -> dict:
        """Get basic stats"""
        memories = self.memory.get_all()
        
        return {
            "total": len(memories),
            "with_tags": sum(1 for m in memories if m.get("tags")),
            "with_priority": sum(1 for m in memories 
                                if m.get("metadata", {}).get("priority")),
        }
    
    def get_tag_distribution(self) -> dict:
        """Get tag distribution"""
        tags = Counter()
        
        for mem in self.memory.get_all():
            tags.update(mem.get("tags", []))
        
        return dict(tags.most_common(20))
    
    def get_content_length_stats(self) -> dict:
        """Content length stats"""
        lengths = [len(m.get("content", "")) for m in self.memory.get_all()]
        
        if not lengths:
            return {}
        
        return {
            "avg": sum(lengths) / len(lengths),
            "min": min(lengths),
            "max": max(lengths),
        }


def demo():
    """Demo analytics"""
    memory = Memory(storage="json", path="./analytics_demo2.json")
    
    memory.add("Short")
    memory.add("Medium length content")
    memory.add("Very long content " * 10, tags=["long"])
    
    analytics = MemoryAnalytics(memory)
    
    print("=== Analytics Demo ===\n")
    print(f"Stats: {analytics.get_stats()}")
    print(f"Tag dist: {analytics.get_tag_distribution()}")
    print(f"Length: {analytics.get_content_length_stats()}")
    
    import os
    if os.path.exists("./analytics_demo2.json"):
        os.remove("./analytics_demo2.json")


if __name__ == "__main__":
    demo()
