"""
Memory Facade
Facade pattern for memory
"""
from memory import Memory


class MemoryFacade:
    """Facade for memory"""
    
    def __init__(self):
        self.memory = Memory(storage="json", path="./facade_memory.json")
    
    def quick_add(self, text: str):
        """Quick add"""
        return self.memory.add(text)
    
    def quick_search(self, query: str):
        """Quick search"""
        return self.memory.search(query)
    
    def quick_get_all(self):
        """Quick get all"""
        return self.memory.get_all()
    
    def quick_delete(self, mem_id: str):
        """Quick delete"""
        return self.memory.forget(mem_id)


# Convenience functions
_add = lambda t: MemoryFacade().quick_add(t)
_search = lambda q: MemoryFacade().quick_search(q)


def demo():
    """Demo facade"""
    facade = MemoryFacade()
    
    facade.quick_add("Test")
    print(f"Count: {len(facade.quick_get_all())}")


if __name__ == "__main__":
    demo()
