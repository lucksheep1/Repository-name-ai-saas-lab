"""
Memory pathlib_example
pathlib_example
"""
from pathlib import Path


def demo():
    print(Path(".").resolve())


if __name__ == "__main__":
    demo()
