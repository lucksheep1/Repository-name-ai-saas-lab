"""
Memory typing_example16
typing_example16
"""
from typing import Dict, Any


def process(data: Dict[str, Any]) -> str:
    return f"Received {len(data)} items"


def demo():
    result = process({"name": "Alice", "age": 30})
    print(result)


if __name__ == "__main__":
    demo()
