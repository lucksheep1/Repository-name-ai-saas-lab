"""
Memory JSON Dump
JSON dump
"""
from memory import Memory
import json


def demo():
    data = {"test": 123}
    print(json.dumps(data))


if __name__ == "__main__":
    demo()
