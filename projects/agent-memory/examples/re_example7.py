"""
Memory re_example7
re_example7
"""
import re


def demo():
    pattern = r"\d+"
    text = "abc123def456"
    print(re.findall(pattern, text))


if __name__ == "__main__":
    demo()
