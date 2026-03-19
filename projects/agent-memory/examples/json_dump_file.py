"""
Memory JSON Dump File
JSON dump file
"""
from memory import Memory
import json


def demo():
    data = {"test": 123}
    with open("test.json", "w") as f:
        json.dump(data, f)
    print("Dumped")


if __name__ == "__main__":
    demo()
