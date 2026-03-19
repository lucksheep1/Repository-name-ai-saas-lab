"""
Memory TX
Transaction support
"""
from memory import Memory


class Transaction:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.ops = []
    
    def add(self, content: str):
        self.ops.append(("add", content))
    
    def delete(self, mem_id: str):
        self.ops.append(("delete", mem_id))
    
    def commit(self):
        for op, data in self.ops:
            if op == "add":
                self.memory.add(data)
            elif op == "delete":
                self.memory.forget(data)
        
        self.ops.clear()
    
    def rollback(self):
        self.ops.clear()


def demo():
    memory = Memory(storage="json", path="./tx_demo.json")
    tx = Transaction(memory)
    
    tx.add("Test1")
    tx.add("Test2")
    tx.commit()
    
    print(f"Count: {len(memory.get_all())}")


if __name__ == "__main__":
    demo()
