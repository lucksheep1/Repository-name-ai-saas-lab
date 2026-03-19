"""
Memory Literal
Literal types
"""
from memory import Memory
from typing import Literal


def status(code: Literal[200, 201, 400, 404, 500]) -> str:
    return f"Status: {code}"


def demo():
    print(status(200))


if __name__ == "__main__":
    demo()
