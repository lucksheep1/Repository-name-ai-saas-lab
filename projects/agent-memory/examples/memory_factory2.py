"""
Memory Factory
Factory methods
"""
from memory import Memory


class Factory:
    @staticmethod
    def create_json(path: str = "memory.json"):
        return Memory(storage="json", path=path)
    
    @staticmethod
    def create_sqlite(path: str = "memory.db"):
        return Memory(storage="sqlite", path=path)


def demo():
    mem = Factory.create_json()
    print(f"Created: {mem}")


if __name__ == "__main__":
    demo()
