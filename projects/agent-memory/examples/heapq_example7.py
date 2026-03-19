"""
Memory heapq_example7
heapq_example7
"""
import heapq


def demo():
    heap = [3, 1, 4, 1, 5, 9, 2, 6]
    heapq.heapify(heap)
    print(heap[0])


if __name__ == "__main__":
    demo()
