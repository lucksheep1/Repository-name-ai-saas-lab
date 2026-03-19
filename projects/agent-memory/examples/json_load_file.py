"""
Memory JSON Load File
JSON load file
"""
from memory import Memory
import json


def demo():
    with open("test.json", "w") as f:
        json.dump({"test": 123}, f)
    with open("test.json", "r") as f:
        print(json.load(f))


if __name__ == "__main__":
    demo()
