"""
Memory Composite
Composite memory patterns
"""
from memory import Memory


class CompositeMemory:
    """Composite memory patterns"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def add_with_metadata(self, content: str, meta: dict):
        """Add with metadata"""
        return self.memory.add(content, metadata=meta)
    
    def add_with_priority(self, content: str, priority: int):
        """Add with priority"""
        return self.memory.add(content, metadata={"priority": priority})
    
    def add_with_timestamp(self, content: str):
        """Add with custom timestamp"""
        from datetime import datetime
        return self.memory.add(content, metadata={"created": datetime.now().isoformat()})


def demo():
    """Demo composite"""
    memory = Memory(storage="json", path="./composite_demo.json")
    composite = CompositeMemory(memory)
    
    composite.add_with_priority("Important", 5)
    composite.add_with_metadata("Test", {"key": "value"})
    
    print(f"Total: {len(memory.get_all())}")


if __name__ == "__main__":
    demo()
