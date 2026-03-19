"""
Memory re_example8
re_example8
"""
import re


def demo():
    text = "hello123world456"
    numbers = re.findall(r"\d+", text)
    print(numbers)


if __name__ == "__main__":
    demo()
