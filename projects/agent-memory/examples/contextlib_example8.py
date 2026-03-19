"""
Memory contextlib_example8
contextlib_example8
"""
from contextlib import suppress


def demo():
    with suppress(ZeroDivisionError):
        print(1/0)
    print("continued")


if __name__ == "__main__":
    demo()
