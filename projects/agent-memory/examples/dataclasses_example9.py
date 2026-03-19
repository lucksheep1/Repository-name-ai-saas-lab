"""
Memory dataclasses_example9
dataclasses_example9
"""
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int
    
    def is_adult(self) -> bool:
        return self.age >= 18


def demo():
    u = User("Alice", 30)
    print(u.is_adult())


if __name__ == "__main__":
    demo()
