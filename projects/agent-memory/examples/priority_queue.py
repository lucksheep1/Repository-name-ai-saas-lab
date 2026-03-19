"""
Memory Priority Queue
Process memories by priority
"""
from agent_memory import Memory
from collections import defaultdict


class PriorityQueue:
    """Memory organized by priority"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def get_by_priority(self, min_priority: int = 1, max_priority: int = 5) -> list:
        """Get memories in priority range"""
        all_mem = self.memory.get_all()
        result = []
        
        for mem in all_mem:
            priority = mem.get("metadata", {}).get("priority", 0)
            if min_priority <= priority <= max_priority:
                result.append(mem)
        
        # Sort by priority descending
        result.sort(key=lambda m: m.get("metadata", {}).get("priority", 0), reverse=True)
        return result
    
    def get_next(self) -> dict:
        """Get highest priority memory"""
        by_priority = self.get_by_priority(1, 5)
        return by_priority[0] if by_priority else None
    
    def reprioritize(self, mem_id: str, new_priority: int):
        """Change priority"""
        mem = self.memory.get(mem_id)
        if mem:
            metadata = mem.get("metadata", {})
            metadata["priority"] = new_priority
            self.memory.update(mem_id, metadata=metadata)


class WeightedMemory:
    """Memory with weighted retrieval"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def get_weighted(self, weights: dict = None) -> list:
        """Get memories with weighted scoring
        
        weights: {"recency": 0.3, "priority": 0.5, "tags": 0.2}
        """
        weights = weights or {"recency": 0.3, "priority": 0.5, "tags": 0.2}
        
        all_mem = self.memory.get_all()
        scored = []
        
        for mem in all_mem:
            score = 0
            
            # Priority weight
            priority = mem.get("metadata", {}).get("priority", 0)
            score += (priority / 5.0) * weights.get("priority", 0)
            
            # Tag weight
            tags = mem.get("tags", [])
            score += len(tags) * 0.1 * weights.get("tags", 0)
            
            scored.append((score, mem))
        
        # Sort by score
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored]


def demo():
    """Demo priority queue"""
    memory = Memory(storage="json", path="./priority_demo.json")
    pq = PriorityQueue(memory)
    
    print("=== Priority Queue Demo ===\n")
    
    # Add with priorities
    memory.add("Low priority task", metadata={"priority": 1})
    memory.add("Medium task", metadata={"priority": 3})
    memory.add("High priority!", metadata={"priority": 5})
    memory.add("Another medium", metadata={"priority": 4})
    
    # Get by priority
    high = pq.get_by_priority(4, 5)
    print(f"High priority ({len(high)}):")
    for m in high:
        p = m.get("metadata", {}).get("priority")
        print(f"  [{p}] {m.get('content', '')[:30]}")
    
    # Get next to process
    next_mem = pq.get_next()
    print(f"\nNext to process: {next_mem.get('content', '')[:30]}")
    
    # Weighted retrieval
    wm = WeightedMemory(memory)
    weighted = wm.get_weighted({"priority": 0.7, "recency": 0.2, "tags": 0.1})
    print(f"\nWeighted (top 3):")
    for m in weighted[:3]:
        print(f"  {m.get('content', '')[:30]}")
    
    # Cleanup
    import os
    if os.path.exists("./priority_demo.json"):
        os.remove("./priority_demo.json")


if __name__ == "__main__":
    demo()
