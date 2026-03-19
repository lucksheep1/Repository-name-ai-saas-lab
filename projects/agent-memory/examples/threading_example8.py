"""
Memory threading_example8
threading_example8
"""
import threading


def worker(msg):
    print(msg)


def demo():
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(f"thread {i}",))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    demo()
