"""
Memory pathlib_example22
pathlib_example22
"""
from pathlib import Path


def demo():
    p = Path(".")
    print([x for x in p.iterdir() if x.is_file()][:3])


if __name__ == "__main__":
    demo()
