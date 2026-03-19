"""
Memory dataclasses_example8
dataclasses_example8
"""
from dataclasses import dataclass


@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080


def demo():
    c = Config()
    print(c.host, c.port)


if __name__ == "__main__":
    demo()
