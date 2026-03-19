"""
Memory pathlib_example10
pathlib_example10
"""
from pathlib import Path


def demo():
    p = Path("/tmp/file.txt")
    print(p.exists())


if __name__ == "__main__":
    demo()
