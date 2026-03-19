"""
Memory urllib_example3
urllib_example3
"""
from urllib.parse import quote, unquote


def demo():
    encoded = quote("hello world")
    decoded = unquote(encoded)
    print(encoded, decoded)


if __name__ == "__main__":
    demo()
