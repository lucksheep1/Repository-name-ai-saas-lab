"""
Memory textwrap_example4
textwrap_example4
"""
import textwrap


def demo():
    text = "This is a very long line that needs to be wrapped."
    print(textwrap.fill(text, width=20))


if __name__ == "__main__":
    demo()
