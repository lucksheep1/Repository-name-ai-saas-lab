"""
Memory pathlib_example14
pathlib_example14
"""
from pathlib import Path


def demo():
    p = Path("/tmp/file.txt")
    print(p.is_dir())


if __name__ == "__main__":
    demo()
