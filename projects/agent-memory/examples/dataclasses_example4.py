"""
Memory dataclasses_example4
dataclasses_example4
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class Team:
    name: str
    members: List[str] = field(default_factory=list)


def demo():
    team = Team("Engineering", ["Alice", "Bob"])
    print(team)


if __name__ == "__main__":
    demo()
