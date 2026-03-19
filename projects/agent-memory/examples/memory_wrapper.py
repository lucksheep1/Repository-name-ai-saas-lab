"""
Memory Wrapper
Wrapper pattern
"""
from memory import Memory


class Wrapper:
    def __init__(self, wrapped):
        self.wrapped = wrapped
    
    def __getattr__(self, name):
        return getattr(self.wrapped, name)


def demo():
    mem = Memory(storage="json", path="test.json")
    wrapped = Wrapper(mem)
    print(wrapped.add("Test"))


if __name__ == "__main__":
    demo()
