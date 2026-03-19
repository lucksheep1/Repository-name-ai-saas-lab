"""
Memory re_example6
re_example6
"""
import re


def demo():
    text = "Price: $19.99"
    match = re.search(r"\$(\d+\.\d+)", text)
    if match:
        print(match.group(1))


if __name__ == "__main__":
    demo()
