"""
Memory pathlib_example3
pathlib_example3
"""
from pathlib import Path


def demo():
    p = Path("/tmp/test.txt")
    p.write_text("hello")
    print(p.read_text())


if __name__ == "__main__":
    demo()
