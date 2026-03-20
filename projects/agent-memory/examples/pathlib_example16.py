"""
Memory pathlib_example16
pathlib_example16
"""
from pathlib import Path
import os


def demo():
    home = Path.home()
    print(f"Home: {home}")
    print(f"Exists: {home.exists()}")


if __name__ == "__main__":
    demo()
