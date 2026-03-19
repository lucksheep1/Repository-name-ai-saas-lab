"""
Memory pathlib_example5
pathlib_example5
"""
from pathlib import Path


def demo():
    p = Path("/tmp/test.txt")
    p.parent.mkdir(parents=True, exist_ok=True)
    print(p.exists())


if __name__ == "__main__":
    demo()
