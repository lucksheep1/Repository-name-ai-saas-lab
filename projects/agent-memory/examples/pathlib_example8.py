"""
Memory pathlib_example8
pathlib_example8
"""
from pathlib import Path


def demo():
    p = Path("/tmp/test")
    p.mkdir(parents=True, exist_ok=True)
    print(p.exists())


if __name__ == "__main__":
    demo()
