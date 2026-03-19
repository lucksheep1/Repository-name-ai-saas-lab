"""
Memory Builder
Builder pattern for memory
"""
from memory import Memory


class MemoryBuilder:
    """Builder for memory"""
    
    def __init__(self):
        self.content = ""
        self.tags = []
        self.metadata = {}
        self.priority = None
    
    def with_content(self, content: str):
        self.content = content
        return self
    
    def with_tag(self, tag: str):
        self.tags.append(tag)
        return self
    
    def with_tags(self, tags: list):
        self.tags.extend(tags)
        return self
    
    def with_metadata(self, key: str, value):
        self.metadata[key] = value
        return self
    
    def with_priority(self, priority: int):
        self.priority = priority
        return self
    
    def build(self, memory: Memory):
        return memory.add(
            self.content,
            tags=self.tags,
            metadata=self.metadata,
            priority=self.priority
        )


def demo():
    """Demo builder"""
    memory = Memory(storage="json", path="./builder_demo.json")
    builder = MemoryBuilder()
    
    builder.with_content("Test").with_tag("demo").with_priority(5).build(memory)
    
    print(f"Total: {len(memory.get_all())}")


if __name__ == "__main__":
    demo()
