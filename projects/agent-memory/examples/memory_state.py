"""
Memory State
State pattern for memory
"""
from memory import Memory


class MemoryState:
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def get_state(self):
        return {"count": len(self.memory.get_all())}


class ActiveState(MemoryState):
    def add(self, content: str):
        return self.memory.add(content)


class ReadOnlyState(MemoryState):
    def add(self, content: str):
        raise Exception("Read only mode")


class StatefulMemory:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.state = ActiveState(memory)
    
    def set_state(self, state: MemoryState):
        self.state = state
    
    def add(self, content: str):
        return self.state.add(content)


def demo():
    memory = Memory(storage="json", path="./state_demo.json")
    sm = StatefulMemory(memory)
    
    sm.add("Test")
    print(f"Count: {sm.state.get_state()}")


if __name__ == "__main__":
    demo()
