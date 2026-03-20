"""
Memory pathlib_example15
pathlib_example15
"""
from pathlib import Path


def demo():
    p = Path("/tmp/test.txt")
    print(p.read_text()[:20] if p.exists() else "file not found")


if __name__ == "__main__":
    demo()
