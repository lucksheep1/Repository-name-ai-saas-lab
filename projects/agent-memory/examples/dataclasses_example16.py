"""
Memory dataclasses_example16
dataclasses_example16
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class Team:
    name: str
    members: List[str] = field(default_factory=list)
    score: int = 0


def demo():
    team = Team(" Warriors", members=["Alice", "Bob"])
    team.score = 10
    print(f"{team.name}: {team.score} points")


if __name__ == "__main__":
    demo()
