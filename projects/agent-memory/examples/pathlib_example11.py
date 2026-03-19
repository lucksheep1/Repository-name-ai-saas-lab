"""
Memory pathlib_example11
pathlib_example11
"""
from pathlib import Path


def demo():
    p = Path("/tmp/test.txt")
    print(p.with_suffix(".md"))


if __name__ == "__main__":
    demo()
