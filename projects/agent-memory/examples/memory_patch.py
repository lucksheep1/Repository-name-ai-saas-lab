"""
Memory Patch
Patch memories
"""
from memory import Memory


class Patch:
    def __init__(self, ops: list):
        self.ops = ops
    
    def apply(self, memory: Memory):
        for op in self.ops:
            if op["op"] == "add":
                memory.add(op["content"], tags=op.get("tags", []))
            elif op["op"] == "remove":
                memory.forget(op["id"])


def demo():
    memory = Memory(storage="json", path="./patch_demo.json")
    
    patch = Patch([
        {"op": "add", "content": "Test1"},
        {"op": "add", "content": "Test2", "tags": ["demo"]}
    ])
    
    patch.apply(memory)
    print(f"Count: {len(memory.get_all())}")


if __name__ == "__main__":
    demo()
