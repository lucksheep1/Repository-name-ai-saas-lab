"""
Memory queue_example12
queue_example12
"""
from queue import PriorityQueue


def demo():
    pq = PriorityQueue()
    pq.put((2, "low"))
    pq.put((1, "high"))
    pq.put((3, "medium"))
    while not pq.empty():
        print(pq.get()[1])


if __name__ == "__main__":
    demo()
