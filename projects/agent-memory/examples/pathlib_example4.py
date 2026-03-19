"""
Memory pathlib_example4
pathlib_example4
"""
from pathlib import Path


def demo():
    p = Path("/tmp/test_dir")
    p.mkdir(exist_ok=True)
    print(p.exists())


if __name__ == "__main__":
    demo()
