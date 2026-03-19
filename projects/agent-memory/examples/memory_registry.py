"""
Memory Registry
Registry pattern for memory
"""
from memory import Memory


class MemoryRegistry:
    """Registry for memories"""
    _registry = {}
    
    @classmethod
    def register(cls, name: str, memory: Memory):
        cls._registry[name] = memory
    
    @classmethod
    def get(cls, name: str) -> Memory:
        return cls._registry.get(name)
    
    @classmethod
    def list_all(cls):
        return list(cls._registry.keys())


def demo():
    mem1 = Memory(storage="json", path="./reg1.json")
    mem2 = Memory(storage="json", path="./reg2.json")
    
    MemoryRegistry.register("primary", mem1)
    MemoryRegistry.register("secondary", mem2)
    
    print(f"Registered: {MemoryRegistry.list_all()}")


if __name__ == "__main__":
    demo()
