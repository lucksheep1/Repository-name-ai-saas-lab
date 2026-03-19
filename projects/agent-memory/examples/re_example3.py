"""
Memory re_example3
re_example3
"""
import re


def demo():
    pattern = r"(\d+)-(\d+)-(\d+)"
    text = "2024-03-19"
    match = re.match(pattern, text)
    if match:
        print(match.groups())


if __name__ == "__main__":
    demo()
