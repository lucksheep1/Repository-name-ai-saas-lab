"""
Memory re_example14
re_example14
"""
import re


def demo():
    text = "hello123world456"
    numbers = re.findall(r"\d+", text)
    print(sum(int(n) for n in numbers))


if __name__ == "__main__":
    demo()
