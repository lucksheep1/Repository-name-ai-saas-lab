"""
Memory Base
Base classes
"""
from memory import Memory


class Base:
    def __init__(self, memory: Memory):
        self.memory = memory


class AddMixin:
    def add(self, content: str):
        return self.memory.add(content)


class SearchMixin:
    def search(self, query: str):
        return self.memory.search(query)


class Extended(AddMixin, SearchMixin, Base):
    pass


def demo():
    print("Extended ready")


if __name__ == "__main__":
    demo()
