"""
Memory Memento
Memento pattern for memory
"""
from memory import Memory


class Memento:
    def __init__(self, state: dict):
        self.state = state
    
    def get_state(self):
        return self.state


class Originator:
    def __init__(self):
        self.memory = Memory(storage="json", path="./memento.json")
    
    def save(self):
        return Memento(self.memory.get_all())
    
    def restore(self, memento: Memento):
        # Clear and restore
        for mem in self.memory.get_all():
            self.memory.forget(mem["id"])
        
        for item in memento.get_state():
            self.memory.add(item.get("content", ""), tags=item.get("tags", []))


def demo():
    orig = Originator()
    orig.memory.add("Test")
    
    memento = orig.save()
    
    orig.memory.add("Another")
    print(f"Before: {len(orig.memory.get_all())}")
    
    orig.restore(memento)
    print(f"After: {len(orig.memory.get_all())}")


if __name__ == "__main__":
    demo()
