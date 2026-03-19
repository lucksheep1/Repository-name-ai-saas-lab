"""
Memory Mapping
Mapping types
"""
from memory import Memory
from typing import Mapping, Dict


def process(mapping: Mapping[str, int]) -> int:
    return sum(mapping.values())


def demo():
    print(process({"a": 1, "b": 2}))


if __name__ == "__main__":
    demo()
