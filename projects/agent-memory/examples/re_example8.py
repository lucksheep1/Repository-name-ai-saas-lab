"""
Memory re_example8
re_example8
"""
import re


def demo():
    text = "Price: $19.99, Tax: $1.50"
    prices = re.findall(r"\$(\d+\.\d+)", text)
    print(prices)


if __name__ == "__main__":
    demo()
