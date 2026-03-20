"""
Memory os_example12
os_example12
"""
import os


def demo():
    print(os.getenv("HOME", "/"))


if __name__ == "__main__":
    demo()
