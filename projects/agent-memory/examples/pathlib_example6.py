"""
Memory pathlib_example6
pathlib_example6
"""
from pathlib import Path


def demo():
    p = Path("/tmp/test.txt")
    print(p.suffix)


if __name__ == "__main__":
    demo()
