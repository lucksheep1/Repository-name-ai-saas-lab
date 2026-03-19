"""
Memory threading_example3
threading_example3
"""
import threading


def demo():
    lock = threading.Lock()
    with lock:
        print("locked")


if __name__ == "__main__":
    demo()
