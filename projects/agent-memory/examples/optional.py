"""
Memory Optional
Optional types
"""
from memory import Memory
from typing import Optional


def get_content(mem: Optional[Memory]) -> Optional[str]:
    if mem is None:
        return None
    return mem.add("test")


def demo():
    print(get_content(None))


if __name__ == "__main__":
    demo()
