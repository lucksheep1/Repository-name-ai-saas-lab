"""
Memory Slots
Slots optimization
"""
from memory import Memory


class SlotsMemory:
    __slots__ = ["memory", "name"]
    
    def __init__(self, name="default"):
        self.name = name
        self.memory = Memory(storage="json", path=f"{name}.json")


def demo():
    mem = SlotsMemory("test")
    print(mem.name)


if __name__ == "__main__":
    demo()
