"""
Memory Unit of Work
Unit of Work pattern
"""
from memory import Memory


class UnitOfWork:
    def __init__(self):
        self.memory = Memory(storage="json", path="./uow.json")
        self.new = []
        self.dirty = []
        self.removed = []
    
    def register_new(self, content: str):
        self.new.append(content)
    
    def register_dirty(self, mem_id: str):
        if mem_id not in self.dirty:
            self.dirty.append(mem_id)
    
    def register_removed(self, mem_id: str):
        self.removed.append(mem_id)
    
    def commit(self):
        for content in self.new:
            self.memory.add(content)
        
        for mem_id in self.removed:
            self.memory.forget(mem_id)
        
        self.new.clear()
        self.dirty.clear()
        self.removed.clear()


def demo():
    uow = UnitOfWork()
    
    uow.register_new("Test1")
    uow.register_new("Test2")
    uow.commit()
    
    print(f"Count: {len(uow.memory.get_all())}")


if __name__ == "__main__":
    demo()
