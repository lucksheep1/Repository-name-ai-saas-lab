"""
Memory Pathlib
Pathlib utilities
"""
from memory import Memory
from pathlib import Path


def demo():
    p = Path(".")
    print(list(p.glob("*.py"))[:3])


if __name__ == "__main__":
    demo()
