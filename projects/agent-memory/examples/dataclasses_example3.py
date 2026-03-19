"""
Memory dataclasses_example3
dataclasses_example3
"""
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int
    email: str = "unknown"


def demo():
    user = User("Alice", 30)
    print(user)


if __name__ == "__main__":
    demo()
