"""
Memory Static
Static method
"""
from memory import Memory


class StaticMemory:
    @staticmethod
    def create():
        return Memory(storage="json", path="static.json")
    
    @staticmethod
    def create_sqlite():
        return Memory(storage="sqlite", path="static.db")


def demo():
    mem = StaticMemory.create()
    print(mem.add("Test"))


if __name__ == "__main__":
    demo()
