"""
Memory Adapter
Adapter pattern for memory
"""
from memory import Memory


class LegacySystem:
    """Legacy system"""
    def __init__(self):
        self.data = []
    
    def store(self, text: str):
        self.data.append(text)
    
    def retrieve(self, query: str):
        return [d for d in self.data if query in d.lower()]


class MemoryAdapter:
    """Adapter for legacy system"""
    
    def __init__(self, legacy: LegacySystem):
        self.legacy = legacy
    
    def add(self, content: str, **kwargs):
        self.legacy.store(content)
        return content
    
    def search(self, query: str):
        return [{"content": d} for d in self.legacy.retrieve(query)]
    
    def get_all(self):
        return [{"content": d} for d in self.legacy.data]


def demo():
    """Demo adapter"""
    legacy = LegacySystem()
    adapter = MemoryAdapter(legacy)
    
    adapter.add("Test")
    print(f"Found: {len(adapter.search('test'))}")


if __name__ == "__main__":
    demo()
