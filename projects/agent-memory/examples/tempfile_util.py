"""
Memory tempfile
tempfile utilities
"""
import tempfile


def demo():
    with tempfile.TemporaryDirectory() as td:
        print(td)


if __name__ == "__main__":
    demo()
