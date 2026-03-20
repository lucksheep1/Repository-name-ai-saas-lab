"""
Memory dataclasses_example12
dataclasses_example12
"""
from dataclasses import dataclass, field


@dataclass
class Container:
    items: list = field(default_factory=list)
    count: int = 0


def demo():
    c = Container()
    c.items.append(1)
    print(c)


if __name__ == "__main__":
    demo()
