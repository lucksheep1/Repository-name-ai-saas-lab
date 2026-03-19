"""
Memory Monkey
Monkey patching
"""
from memory import Memory


def patched_add(self, content):
    return self.add(f"[PATCHED] {content}")


original_add = Memory.add
Memory.add = patched_add


def demo():
    mem = Memory(storage="json", path="test.json")
    print(mem.add("Test"))


if __name__ == "__main__":
    demo()
