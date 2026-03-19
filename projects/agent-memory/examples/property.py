"""
Memory Property
Property decorator
"""
from memory import Memory


class PropertyMemory:
    def __init__(self):
        self._memory = None
    
    @property
    def memory(self):
        if self._memory is None:
            self._memory = Memory(storage="json", path="prop.json")
        return self._memory


def demo():
    pm = PropertyMemory()
    print(pm.memory.add("Test"))


if __name__ == "__main__":
    demo()
