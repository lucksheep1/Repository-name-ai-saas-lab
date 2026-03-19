"""
Memory Command
Command pattern for memory
"""
from memory import Memory


class Command:
    """Command"""
    def execute(self):
        raise NotImplementedError


class AddCommand(Command):
    def __init__(self, memory: Memory, content: str):
        self.memory = memory
        self.content = content
    
    def execute(self):
        return self.memory.add(self.content)


class SearchCommand(Command):
    def __init__(self, memory: Memory, query: str):
        self.memory = memory
        self.query = query
    
    def execute(self):
        return self.memory.search(self.query)


class CommandQueue:
    def __init__(self):
        self.queue = []
    
    def add(self, cmd: Command):
        self.queue.append(cmd)
    
    def execute_all(self):
        results = []
        for cmd in self.queue:
            results.append(cmd.execute())
        self.queue.clear()
        return results


def demo():
    memory = Memory(storage="json", path="./command_demo.json")
    queue = CommandQueue()
    
    queue.add(AddCommand(memory, "Test1"))
    queue.add(AddCommand(memory, "Test2"))
    
    results = queue.execute_all()
    print(f"Added: {len(results)}")


if __name__ == "__main__":
    demo()
