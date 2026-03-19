"""
Memory pathlib_example8
pathlib_example8
"""
from pathlib import Path


def demo():
    p = Path("/tmp/test.txt")
    print(p.stem, p.suffix)


if __name__ == "__main__":
    demo()
