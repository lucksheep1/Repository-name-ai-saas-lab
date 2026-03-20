"""
Memory pathlib_example12
pathlib_example12
"""
from pathlib import Path


def demo():
    p = Path("/tmp/test.txt")
    print(p.is_file())


if __name__ == "__main__":
    demo()
