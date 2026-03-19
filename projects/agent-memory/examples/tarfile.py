"""
Memory tarfile
tarfile utilities
"""
from memory import Memory
import tarfile


def demo():
    with tarfile.open("test.tar", "w") as tf:
        pass
    print("Created tar")


if __name__ == "__main__":
    demo()
