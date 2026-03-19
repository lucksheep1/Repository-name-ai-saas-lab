"""
Memory os_example4
os_example4
"""
import os


def demo():
    print(os.environ.get("HOME", "/"))


if __name__ == "__main__":
    demo()
