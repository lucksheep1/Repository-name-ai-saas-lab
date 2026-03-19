"""
Memory queue_example3
queue_example3
"""
from queue import PriorityQueue


def demo():
    pq = PriorityQueue()
    pq.put((1, "first"))
    pq.put((0, "second"))
    print(pq.get()[1])


if __name__ == "__main__":
    demo()
