"""
Memory Singleton
Singleton pattern for memory
"""
from memory import Memory


class SingletonMemory:
    """Singleton memory"""
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.memory = Memory(*args, **kwargs)
        return cls._instance
    
    def __getattr__(self, name):
        return getattr(self.memory, name)


def demo():
    """Demo singleton"""
    mem1 = SingletonMemory(storage="json", path="./singleton.json")
    mem2 = SingletonMemory(storage="json", path="./singleton.json")
    
    mem1.add("Test")
    
    print(f"Same instance: {mem1 is mem2}")
    print(f"Count: {len(mem2.get_all())}")


if __name__ == "__main__":
    demo()
