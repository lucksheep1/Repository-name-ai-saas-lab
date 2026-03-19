"""
Memory Controller
Controller pattern
"""
from memory import Memory


class Controller:
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def add(self, request):
        content = request.get("content", "")
        return self.memory.add(content)
    
    def search(self, request):
        query = request.get("query", "")
        return self.memory.search(query)


def demo():
    controller = Controller(Memory(storage="json", path="test.json"))
    print(controller.add({"content": "Test"}))


if __name__ == "__main__":
    demo()
