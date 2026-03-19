"""
Memory zipfile
zipfile utilities
"""
from memory import Memory
import zipfile


def demo():
    with zipfile.ZipFile("test.zip", "w") as zf:
        pass
    print("Created zip")


if __name__ == "__main__":
    demo()
