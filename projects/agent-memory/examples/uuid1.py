"""
Memory UUID1
UUID version 1
"""
from memory import Memory
import uuid


def demo():
    id = uuid.uuid1()
    print(id)


if __name__ == "__main__":
    demo()
