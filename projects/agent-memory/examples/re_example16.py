"""
Memory re_example16
re_example16
"""
import re


def demo():
    text = "The quick brown fox"
    pattern = r"(\w+) (\w+)"
    match = re.search(pattern, text)
    if match:
        print(match.group(1), match.group(2))


if __name__ == "__main__":
    demo()
