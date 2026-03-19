"""
Memory typing_example7
typing_example7
"""
from typing import Dict, List, Optional


def process(data: Dict[str, List[int]]) -> Optional[int]:
    return sum(data.get("values", []))


def demo():
    print(process({"values": [1, 2, 3]}))


if __name__ == "__main__":
    demo()
