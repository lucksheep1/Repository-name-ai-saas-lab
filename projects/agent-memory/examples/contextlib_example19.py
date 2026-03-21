"""
Memory contextlib_example19
contextlib_example19
"""
from contextlib import closing


def demo():
    with closing(open("test.txt", "w")) as f:
        f.write("test")


if __name__ == "__main__":
    demo()
