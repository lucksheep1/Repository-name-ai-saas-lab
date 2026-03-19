"""
Memory re_example10
re_example10
"""
import re


def demo():
    text = "The quick brown fox"
    pattern = r"quick.*fox"
    match = re.search(pattern, text)
    print(match.group() if match else "no match")


if __name__ == "__main__":
    demo()
