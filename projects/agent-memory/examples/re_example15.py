"""
Memory re_example15
re_example15
"""
import re


def demo():
    text = "The price is $19.99"
    match = re.search(r"\$\d+\.\d+", text)
    print(match.group() if match else "no match")


if __name__ == "__main__":
    demo()
