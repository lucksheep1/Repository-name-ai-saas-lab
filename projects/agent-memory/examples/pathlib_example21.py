"""
Memory pathlib_example21
pathlib_example21
"""
from pathlib import Path


def demo():
    p = Path("test.txt")
    p.touch()
    print(p.exists())
    p.unlink()


if __name__ == "__main__":
    demo()
