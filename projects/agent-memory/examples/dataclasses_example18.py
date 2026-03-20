"""
Memory dataclasses_example18
dataclasses_example18
"""
from dataclasses import dataclass, field


@dataclass
class Config:
    name: str = "default"
    timeout: int = 30
    retry: int = 3
    metadata: dict = field(default_factory=dict)


def demo():
    c = Config(name="app", timeout=60)
    c.metadata["version"] = "1.0"
    print(c)


if __name__ == "__main__":
    demo()
