"""
Memory contextlib_example15
contextlib_example15
"""
from contextlib import redirect_stdout
import io


def demo():
    f = io.StringIO()
    with redirect_stdout(f):
        print("Hello")
    print(f.getvalue())


if __name__ == "__main__":
    demo()
