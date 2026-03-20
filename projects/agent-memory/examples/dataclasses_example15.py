"""
Memory dataclasses_example15
dataclasses_example15
"""
from dataclasses import dataclass, asdict


@dataclass
class User:
    name: str
    email: str
    age: int = 0


def demo():
    u = User("Alice", "alice@example.com", 30)
    print(asdict(u))


if __name__ == "__main__":
    demo()
