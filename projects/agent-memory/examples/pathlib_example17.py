"""
Memory pathlib_example17
pathlib_example17
"""
from pathlib import Path


def demo():
    p = Path("/tmp/test.txt")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("Hello")
    print(p.read_text())


if __name__ == "__main__":
    demo()
