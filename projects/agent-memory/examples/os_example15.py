"""
Memory os_example15
os_example15
"""
import os


def demo():
    print(os.getcwd())
    print(os.listdir(".")[:5])


if __name__ == "__main__":
    demo()
