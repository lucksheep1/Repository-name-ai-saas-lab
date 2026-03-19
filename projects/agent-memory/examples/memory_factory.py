"""
Memory Factory
Factory pattern for memory
"""
from memory import Memory


class MemoryFactory:
    """Factory for memory"""
    
    @staticmethod
    def create_json(path: str = "memory.json"):
        return Memory(storage="json", path=path)
    
    @staticmethod
    def create_sqlite(path: str = "memory.db"):
        return Memory(storage="sqlite", path=path)
    
    @staticmethod
    def create_faiss(path: str = "memory.faiss"):
        return Memory(storage="faiss", path=path)


def demo():
    """Demo factory"""
    json_mem = MemoryFactory.create_json()
    sqlite_mem = MemoryFactory.create_sqlite()
    
    json_mem.add("Test")
    
    print(f"JSON: {len(json_mem.get_all())}")
    print(f"SQLite: {len(sqlite_mem.get_all())}")


if __name__ == "__main__":
    demo()
