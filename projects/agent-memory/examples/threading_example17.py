"""
Memory threading_example17
threading_example17
"""
import threading


def worker():
    print("Working")


def demo():
    t = threading.Thread(target=worker)
    t.start()
    t.join()


if __name__ == "__main__":
    demo()
