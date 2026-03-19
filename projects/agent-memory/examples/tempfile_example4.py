"""
Memory tempfile_example4
tempfile_example4
"""
import tempfile


def demo():
    with tempfile.TemporaryDirectory() as td:
        print(td)


if __name__ == "__main__":
    demo()
