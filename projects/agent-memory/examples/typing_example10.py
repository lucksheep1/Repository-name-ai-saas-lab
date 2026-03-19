"""
Memory typing_example10
typing_example10
"""
from typing import Dict, Any


def process(data: Dict[str, Any]) -> str:
    return str(data)


def demo():
    print(process({"key": "value", "num": 42}))


if __name__ == "__main__":
    demo()
