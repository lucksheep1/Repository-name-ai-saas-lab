"""
Memory Mobile API
Mobile-friendly API endpoints
"""
from agent_memory import Memory


class MobileAPI:
    """Mobile-friendly API"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def get_timeline(self, limit: int = 20, offset: int = 0) -> dict:
        """Get timeline for mobile"""
        all_memories = self.memory.get_all()
        
        total = len(all_memories)
        memories = all_memories[offset:offset + limit]
        
        return {
            "success": True,
            "total": total,
            "limit": limit,
            "offset": offset,
            "memories": memories
        }
    
    def search_mobile(self, query: str, limit: int = 10) -> dict:
        """Mobile search"""
        results = self.memory.search(query, limit=limit)
        
        return {
            "success": True,
            "query": query,
            "count": len(results),
            "results": results
        }
    
    def quick_add(self, content: str, tags: str = None) -> dict:
        """Quick add from mobile"""
        tag_list = []
        
        if tags:
            tag_list = [t.strip() for t in tags.split(",")]
        
        mem_id = self.memory.add(content, tags=tag_list)
        
        return {
            "success": True,
            "id": mem_id
        }
    
    def get_stats(self) -> dict:
        """Get memory stats"""
        memories = self.memory.get_all()
        
        tag_counts = {}
        for mem in memories:
            for tag in mem.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        return {
            "success": True,
            "total": len(memories),
            "tags": tag_counts
        }


def demo():
    """Demo mobile API"""
    memory = Memory(storage="json", path="./mobile_demo.json")
    api = MobileAPI(memory)
    
    print("=== Mobile API Demo ===\n")
    
    # Add memories
    memory.add("Test 1", tags=["a", "b"])
    memory.add("Test 2", tags=["a"])
    
    # Timeline
    result = api.get_timeline()
    print(f"Timeline: {result['total']} total")
    
    # Stats
    stats = api.get_stats()
    print(f"Stats: {stats['tags']}")
    
    # Cleanup
    import os
    if os.path.exists("./mobile_demo.json"):
        os.remove("./mobile_demo.json")


if __name__ == "__main__":
    demo()
