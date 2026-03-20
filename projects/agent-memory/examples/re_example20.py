"""
Memory re_example20
re_example20
"""
import re


def demo():
    text = "abc123def456"
    print(re.findall(r"\d+", text))


if __name__ == "__main__":
    demo()
