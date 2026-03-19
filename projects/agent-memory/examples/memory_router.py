"""
Memory Router
Route memories to different storage backends based on rules
"""
from agent_memory import Memory
from typing import Optional


class MemoryRouter:
    """Route memories to different backends based on rules"""
    
    def __init__(self):
        self.routers = []  # (condition, storage_config) pairs
        self.default = Memory(storage="json", path="./default_memory.json")
    
    def add_rule(self, condition: callable, storage: str, **kwargs):
        """Add routing rule
        
        Args:
            condition: Function that returns True for matching memories
            storage: Storage type ('json', 'sqlite')
            **kwargs: Additional storage parameters
        """
        self.routers.append({
            "condition": condition,
            "storage": storage,
            "config": kwargs
        })
    
    def _get_backend(self, content: str, tags: list, metadata: dict) -> Memory:
        """Determine which backend to use"""
        for rule in self.routers:
            if rule["condition"](content, tags, metadata):
                path = rule["config"].get("path", f"./memory_{rule['storage']}.json")
                return Memory(storage=rule["storage"], path=path)
        
        return self.default
    
    def add(self, content: str, tags: list = None, metadata: dict = None, **kwargs):
        """Add memory to appropriate backend"""
        tags = tags or []
        metadata = metadata or {}
        
        backend = self._get_backend(content, tags, metadata)
        return backend.add(content, tags=tags, metadata=metadata, **kwargs)
    
    def search(self, query: str, limit: int = 10):
        """Search across all backends"""
        results = []
        seen_ids = set()
        
        # Search default
        for mem in self.default.search(query, limit=limit):
            if mem["id"] not in seen_ids:
                results.append(mem)
                seen_ids.add(mem["id"])
        
        # Search routers
        for rule in self.routers:
            path = rule["config"].get("path", f"./memory_{rule['storage']}.json")
            backend = Memory(storage=rule["storage"], path=path)
            
            for mem in backend.search(query, limit=limit):
                if mem["id"] not in seen_ids:
                    results.append(mem)
                    seen_ids.add(mem["id"])
        
        return results[:limit]
    
    def get_all(self):
        """Get all memories from all backends"""
        results = []
        
        results.extend(self.default.get_all())
        
        for rule in self.routers:
            path = rule["config"].get("path", f"./memory_{rule['storage']}.json")
            backend = Memory(storage=rule["storage"], path=path)
            results.extend(backend.get_all())
        
        return results


# Example routing rules
def urgent_condition(content: str, tags: list, metadata: dict) -> bool:
    """Route urgent/high priority to SQLite for reliability"""
    if metadata.get("priority", 0) >= 4:
        return True
    if "urgent" in content.lower():
        return True
    if "urgent" in tags:
        return True
    return False


def bug_condition(content: str, tags: list, metadata: dict) -> bool:
    """Route bug-related memories to separate store"""
    if "bug" in tags:
        return True
    if "error" in content.lower():
        return True
    return False


def long_term_condition(content: str, tags: list, metadata: dict) -> bool:
    """Route long-term memories to dedicated store"""
    if metadata.get("ttl_days", 0) >= 30:
        return True
    if "important" in tags:
        return True
    return False


class TieredMemory:
    """Memory with automatic tiering based on age/importance"""
    
    def __init__(self):
        self.hot = Memory(storage="sqlite", path="./memory_hot.db")  # Recent
        self.warm = Memory(storage="json", path="./memory_warm.json")  # Week-old
        self.cold = Memory(storage="json", path="./memory_cold.json")  # Old
    
    def add(self, content: str, **kwargs):
        """Add to hot storage"""
        return self.hot.add(content, **kwargs)
    
    def get_all(self):
        """Get from all tiers"""
        return self.hot.get_all() + self.warm.get_all() + self.cold.get_all()
    
    def promote(self, mem_id: str):
        """Promote memory to hotter tier"""
        # Find in cold and promote to warm
        for mem in self.cold.get_all():
            if mem["id"] == mem_id:
                self.cold.forget(mem_id)
                self.warm.add(mem["content"], tags=mem.get("tags"), 
                             metadata=mem.get("metadata"))
                return True
        return False
    
    def demote(self, mem_id: str):
        """Demote memory to colder tier"""
        # Find in hot and demote to warm
        for mem in self.hot.get_all():
            if mem["id"] == mem_id:
                self.hot.forget(mem_id)
                self.cold.add(mem["content"], tags=mem.get("tags"),
                             metadata=mem.get("metadata"))
                return True
        return False


def demo():
    """Demo memory routing"""
    router = MemoryRouter()
    
    # Add routing rules
    router.add_rule(urgent_condition, "sqlite", path="./urgent_memory.db")
    router.add_rule(bug_condition, "sqlite", path="./bug_memory.db")
    
    print("=== Memory Router Demo ===\n")
    
    # Add various memories
    router.add("Normal conversation", tags=["chat"])
    router.add("Urgent: System down!", tags=["urgent"], priority=5)
    router.add("Bug found in login", tags=["bug"])
    router.add("User preferences saved", tags=["preferences"])
    
    print("Added 4 memories (routed to different backends)\n")
    
    # Search across all
    results = router.search("memory")
    print(f"Search 'memory': {len(results)} results")
    
    # Get all
    all_mem = router.get_all()
    print(f"Total memories: {len(all_mem)}")
    
    # Cleanup demo files
    import os
    for f in ["./default_memory.json", "./urgent_memory.db", 
              "./bug_memory.db", "./memory_sqlite.json"]:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    demo()
