"""
Memory dataclasses_example22
dataclasses_example22
"""
from dataclasses import dataclass, field


@dataclass
class Config:
    name: str
    value: int = 0
    tags: list = field(default_factory=list)


def demo():
    c = Config("test", tags=["a", "b"])
    print(c)


if __name__ == "__main__":
    demo()
