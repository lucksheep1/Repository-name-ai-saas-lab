"""
Memory re_example11
re_example11
"""
import re


def demo():
    text = "email: test@example.com"
    match = re.search(r"[\w.-]+@[\w.-]+", text)
    print(match.group() if match else "no match")


if __name__ == "__main__":
    demo()
