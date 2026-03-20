"""
Memory pathlib_example20
pathlib_example20
"""
from pathlib import Path


def demo():
    p = Path("/tmp")
    print(list(p.iterdir())[:3])


if __name__ == "__main__":
    demo()
