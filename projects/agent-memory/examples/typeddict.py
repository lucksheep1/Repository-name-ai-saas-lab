"""
Memory TypedDict
Typed dictionary
"""
from memory import Memory
from typing import TypedDict


class MemoryDict(TypedDict):
    content: str
    tags: list


def demo():
    data: MemoryDict = {"content": "Test", "tags": ["demo"]}
    print(data)


if __name__ == "__main__":
    demo()
