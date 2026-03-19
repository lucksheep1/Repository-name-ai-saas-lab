"""
Memory re_example4
re_example4
"""
import re


def demo():
    text = "email: test@example.com"
    print(re.findall(r"[\w.-]+@[\w.-]+", text))


if __name__ == "__main__":
    demo()
