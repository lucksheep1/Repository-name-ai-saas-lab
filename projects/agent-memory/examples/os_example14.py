"""
Memory os_example14
os_example14
"""
import os


def demo():
    print(f"PID: {os.getpid()}")
    print(f"UID: {os.getuid()}")


if __name__ == "__main__":
    demo()
