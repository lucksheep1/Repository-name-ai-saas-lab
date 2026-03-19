"""
Memory Extension
Extension methods
"""
from memory import Memory


def extension_method(self, x):
    return x * 2


Memory.extension_method = extension_method


def demo():
    mem = Memory(storage="json", path="test.json")
    print(mem.extension_method(5))


if __name__ == "__main__":
    demo()
