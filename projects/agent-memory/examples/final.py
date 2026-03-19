"""
Memory Class
Final class
"""
from memory import Memory


def final(cls):
    return cls


@final
class FinalMemory:
    def __init__(self):
        self.memory = Memory(storage="json", path="final.json")


def demo():
    print("Final class ready")


if __name__ == "__main__":
    demo()
