"""
Memory re_example9
re_example9
"""
import re


def demo():
    text = "hello123world456"
    numbers = re.findall(r"\d+", text)
    print(numbers)


if __name__ == "__main__":
    demo()
