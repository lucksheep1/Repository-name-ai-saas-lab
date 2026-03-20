"""
Memory dataclasses_example21
dataclasses_example21
"""
from dataclasses import dataclass


@dataclass
class User:
    name: str
    email: str


def demo():
    u = User("Alice", "alice@example.com")
    print(u)


if __name__ == "__main__":
    demo()
