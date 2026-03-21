"""
Memory threading_example20
threading_example20
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
