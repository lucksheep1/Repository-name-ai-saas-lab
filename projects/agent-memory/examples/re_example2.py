"""
Memory re_example2
re_example2
"""
import re


def demo():
    print(re.sub(r"\d+", "NUM", "abc123def"))


if __name__ == "__main__":
    demo()
