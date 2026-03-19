"""
Memory dataclasses_example2
dataclasses_example2
"""
from dataclasses import field


def demo():
    print(field(default_factory=list))


if __name__ == "__main__":
    demo()
