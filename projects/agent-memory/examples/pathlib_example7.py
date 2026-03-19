"""
Memory pathlib_example7
pathlib_example7
"""
from pathlib import Path


def demo():
    p = Path("/tmp/test.txt")
    print(p.with_suffix(".md"))


if __name__ == "__main__":
    demo()
