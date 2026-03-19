"""
Memory Builder
Builder pattern
"""
from memory import Memory


class Builder:
    def __init__(self):
        self.content = ""
        self.tags = []
    
    def content(self, text: str):
        self.content = text
        return self
    
    def tag(self, tag: str):
        self.tags.append(tag)
        return self
    
    def build(self):
        mem = Memory(storage="json", path="build.json")
        return mem.add(self.content, tags=self.tags)


def demo():
    builder = Builder()
    mem = builder.content("Test").tag("demo").build()
    print(f"Built: {mem}")


if __name__ == "__main__":
    demo()
