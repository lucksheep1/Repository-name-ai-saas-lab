"""
Memory re_example17
re_example17
"""
import re


def demo():
    text = "abc123def456"
    numbers = re.findall(r"\d+", text)
    print(numbers)


if __name__ == "__main__":
    demo()
