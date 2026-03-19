"""
Memory pathlib_example9
pathlib_example9
"""
from pathlib import Path


def demo():
    p = Path("/tmp/test.txt")
    print(p.parent.name)


if __name__ == "__main__":
    demo()
