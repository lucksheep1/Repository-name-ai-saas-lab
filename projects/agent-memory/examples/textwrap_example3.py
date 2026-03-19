"""
Memory textwrap_example3
textwrap_example3
"""
import textwrap


def demo():
    text = "This is a very long line that should be wrapped."
    print(textwrap.shorten(text, width=20))


if __name__ == "__main__":
    demo()
