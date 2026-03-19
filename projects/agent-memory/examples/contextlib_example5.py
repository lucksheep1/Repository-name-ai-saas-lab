"""
Memory contextlib_example5
contextlib_example5
"""
from contextlib import redirect_stdout
import io


def demo():
    f = io.StringIO()
    with redirect_stdout(f):
        print("hello")
    print(f.getvalue())


if __name__ == "__main__":
    demo()
