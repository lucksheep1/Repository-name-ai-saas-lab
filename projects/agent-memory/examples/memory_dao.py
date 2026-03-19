"""
Memory DAO
Data Access Object for memory
"""
from memory import Memory


class MemoryDAO:
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def create(self, content: str, tags: list = None):
        return self.memory.add(content, tags=tags or [])
    
    def read(self, mem_id: str):
        return self.memory.get(mem_id)
    
    def read_all(self):
        return self.memory.get_all()
    
    def update(self, mem_id: str, content: str):
        return self.memory.update(mem_id, content=content)
    
    def delete(self, mem_id: str):
        return self.memory.forget(mem_id)
    
    def search(self, query: str):
        return self.memory.search(query)


def demo():
    memory = Memory(storage="json", path="./dao_demo.json")
    dao = MemoryDAO(memory)
    
    dao.create("Test", ["demo"])
    print(f"Count: {len(dao.read_all())}")


if __name__ == "__main__":
    demo()
