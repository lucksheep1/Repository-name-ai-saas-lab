"""
Memory pathlib_example19
pathlib_example19
"""
from pathlib import Path


def demo():
    p = Path("/tmp")
    print(p.exists())


if __name__ == "__main__":
    demo()
