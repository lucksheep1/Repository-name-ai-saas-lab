"""
Memory threading_example2
threading_example2
"""
import threading


def worker(msg):
    print(msg)


def demo():
    t1 = threading.Thread(target=worker, args=("hello",))
    t2 = threading.Thread(target=worker, args=("world",))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    demo()
