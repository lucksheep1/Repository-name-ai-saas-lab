"""
Memory Repository
Repository pattern
"""
from memory import Memory


class Repository:
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def find_all(self):
        return self.memory.get_all()
    
    def find_by_id(self, mem_id: str):
        return self.memory.get(mem_id)
    
    def find_by_tag(self, tag: str):
        return self.memory.get_by_tag(tag)
    
    def save(self, content: str, tags: list = None):
        return self.memory.add(content, tags=tags or [])
    
    def remove(self, mem_id: str):
        return self.memory.forget(mem_id)


def demo():
    repo = Repository(Memory(storage="json", path="./repo_demo.json"))
    
    repo.save("Test", ["demo"])
    print(f"Count: {len(repo.find_all())}")


if __name__ == "__main__":
    demo()
