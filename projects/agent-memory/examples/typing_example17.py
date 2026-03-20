"""
Memory typing_example17
typing_example17
"""
from typing import Optional, Union


def greet(name: Optional[str]) -> str:
    return f"Hello, {name or 'Anonymous'}!"


def demo():
    print(greet("Alice"))
    print(greet(None))


if __name__ == "__main__":
    demo()
