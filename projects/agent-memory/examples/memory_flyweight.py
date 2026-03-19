"""
Memory Flyweight
Flyweight pattern for memory
"""
from memory import Memory


class FlyweightFactory:
    """Flyweight factory"""
    def __init__(self):
        self.memory = Memory(storage="json", path="./flyweight.json")
        self.cache = {}
    
    def get_memory(self, key: str):
        if key not in self.cache:
            self.cache[key] = self.memory
        return self.memory


def demo():
    factory = FlyweightFactory()
    
    m1 = factory.get_memory("default")
    m2 = factory.get_memory("default")
    
    print(f"Same: {m1 is m2}")


if __name__ == "__main__":
    demo()
