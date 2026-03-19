"""
Memory textwrap_example2
textwrap_example2
"""
import textwrap


def demo():
    text = "This is a very long string that needs wrapping"
    print(textwrap.fill(text, width=20))


if __name__ == "__main__":
    demo()
