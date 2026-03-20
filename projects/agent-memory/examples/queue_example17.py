"""
Memory queue_example17
queue_example17
"""
import queue


def demo():
    q = queue.Queue()
    q.put("item")
    print(q.get())


if __name__ == "__main__":
    demo()
