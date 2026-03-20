"""
Memory contextlib_example9
contextlib_example9
"""
from contextlib import closing


def demo():
    with closing(open("/dev/null")) as f:
        print("opened")


if __name__ == "__main__":
    demo()
