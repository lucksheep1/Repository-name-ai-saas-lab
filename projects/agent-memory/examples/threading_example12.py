"""
Memory threading_example12
threading_example12
"""
import threading


def worker():
    print("done")


def demo():
    t = threading.Thread(target=worker)
    t.start()
    t.join()


if __name__ == "__main__":
    demo()
