"""
Memory Re
Regular expressions
"""
from memory import Memory
import re


def demo():
    pattern = r"\d+"
    text = "abc123def456"
    matches = re.findall(pattern, text)
    print(matches)


if __name__ == "__main__":
    demo()
