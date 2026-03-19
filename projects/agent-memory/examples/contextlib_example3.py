"""
Memory contextlib_example3
contextlib_example3
"""
from contextlib import closing


def demo():
    with closing(open("/dev/null")) as f:
        pass


if __name__ == "__main__":
    demo()
