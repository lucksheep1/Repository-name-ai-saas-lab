"""
Memory re_example5
re_example5
"""
import re


def demo():
    pattern = r"(\w+)@(\w+)\.(\w+)"
    email = "user@example.com"
    match = re.match(pattern, email)
    print(match.groups())


if __name__ == "__main__":
    demo()
