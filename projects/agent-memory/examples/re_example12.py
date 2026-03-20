"""
Memory re_example12
re_example12
"""
import re


def demo():
    text = "abc123def456"
    result = re.sub(r"\d+", "NUM", text)
    print(result)


if __name__ == "__main__":
    demo()
