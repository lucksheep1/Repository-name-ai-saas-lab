"""
Memory pathlib_example18
pathlib_example18
"""
from pathlib import Path


def demo():
    p = Path(".")
    print([x.name for x in p.iterdir() if x.is_file()][:3])


if __name__ == "__main__":
    demo()
