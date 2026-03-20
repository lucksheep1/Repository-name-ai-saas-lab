"""
Memory os_example18
os_example18
"""
import os


def demo():
    print(os.environ.get("HOME", "/"))


if __name__ == "__main__":
    demo()
