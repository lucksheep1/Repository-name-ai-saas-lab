"""
Memory heapq_example14
heapq_example14
"""
import heapq


def demo():
    heap = [3, 1, 4, 1, 5]
    heapq.heapify(heap)
    print(heap[0])


if __name__ == "__main__":
    demo()
