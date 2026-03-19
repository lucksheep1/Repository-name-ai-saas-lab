"""
Memory Gateway
Gateway pattern
"""
from memory import Memory


class MemoryGateway:
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def execute(self, command: str, params: dict = None):
        params = params or {}
        
        if command == "add":
            return self.memory.add(params.get("content", ""))
        elif command == "search":
            return self.memory.search(params.get("query", ""))
        elif command == "list":
            return self.memory.get_all()
        elif command == "delete":
            return self.memory.forget(params.get("id", ""))
        
        return None


def demo():
    gateway = MemoryGateway(Memory(storage="json", path="./gateway_demo.json"))
    
    gateway.execute("add", {"content": "Test"})
    print(f"Count: {len(gateway.execute('list'))}")


if __name__ == "__main__":
    demo()
