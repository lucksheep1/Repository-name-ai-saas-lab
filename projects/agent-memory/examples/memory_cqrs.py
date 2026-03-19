"""
Memory CQRS
CQRS pattern
"""
from memory import Memory


class CommandSide:
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def execute(self, cmd: str, params: dict):
        if cmd == "add":
            return self.memory.add(params.get("content", ""))
        elif cmd == "delete":
            return self.memory.forget(params.get("id", ""))


class QuerySide:
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def query(self, q: str, params: dict = None):
        params = params or {}
        
        if q == "all":
            return self.memory.get_all()
        elif q == "search":
            return self.memory.search(params.get("query", ""))


class CQRSMemory:
    def __init__(self, memory: Memory):
        self.command = CommandSide(memory)
        self.query = QuerySide(memory)


def demo():
    memory = Memory(storage="json", path="./cqrs_demo.json")
    cqrs = CQRSMemory(memory)
    
    cqrs.command.execute("add", {"content": "Test"})
    print(f"Query: {len(cqrs.query.query('all'))}")


if __name__ == "__main__":
    demo()
