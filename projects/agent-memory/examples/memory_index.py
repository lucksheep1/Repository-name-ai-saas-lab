"""
Memory Index
Index memory for fast lookup
"""
from memory import Memory


class MemoryIndex:
    """Index memory"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.index = {}
    
    def build(self):
        """Build index"""
        self.index.clear()
        
        for mem in self.memory.get_all():
            words = mem.get("content", "").lower().split()
            
            for word in words:
                if word not in self.index:
                    self.index[word] = []
                
                self.index[word].append(mem["id"])
    
    def search(self, query: str):
        """Search index"""
        words = query.lower().split()
        results = set()
        
        for word in words:
            if word in self.index:
                results.update(self.index[word])
        
        return [self.memory.get(rid) for rid in results]


def demo():
    """Demo index"""
    memory = Memory(storage="json", path="./index_demo.json")
    index = MemoryIndex(memory)
    
    memory.add("Python tutorial")
    index.build()
    
    results = index.search("python")
    print(f"Found: {len(results)}")


if __name__ == "__main__":
    demo()
