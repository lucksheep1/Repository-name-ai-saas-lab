"""
Memory JSON Load
JSON load
"""
from memory import Memory
import json


def demo():
    data = json.loads('{"test": 123}')
    print(data)


if __name__ == "__main__":
    demo()
