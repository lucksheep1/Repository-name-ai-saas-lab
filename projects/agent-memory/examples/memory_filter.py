"""
Memory Filter
Filter memories
"""
from agent_memory import Memory


class MemoryFilter:
    """Filter memories"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def filter_by_tags(self, tags: list, match_all: bool = False):
        """Filter by tags"""
        results = []
        
        for mem in self.memory.get_all():
            mem_tags = set(mem.get("tags", []))
            
            if match_all:
                if all(t in mem_tags for t in tags):
                    results.append(mem)
            else:
                if any(t in mem_tags for t in tags):
                    results.append(mem)
        
        return results
    
    def filter_by_content(self, pattern: str):
        """Filter by content"""
        import re
        
        results = []
        
        for mem in self.memory.get_all():
            if re.search(pattern, mem.get("content", ""), re.I):
                results.append(mem)
        
        return results
    
    def filter_by_metadata(self, key: str, value):
        """Filter by metadata"""
        results = []
        
        for mem in self.memory.get_all():
            if mem.get("metadata", {}).get(key) == value:
                results.append(mem)
        
        return results


def demo():
    """Demo filter"""
    memory = Memory(storage="json", path="./filter_demo.json")
    filter = MemoryFilter(memory)
    
    memory.add("Test 1", tags=["a", "b"])
    memory.add("Test 2", tags=["a"])
    memory.add("Test 3", tags=["b", "c"])
    
    results = filter.filter_by_tags(["a"], match_all=False)
    print(f"Tags [a]: {len(results)}")
    
    import os
    if os.path.exists("./filter_demo.json"):
        os.remove("./filter_demo.json")


if __name__ == "__main__":
    demo()
