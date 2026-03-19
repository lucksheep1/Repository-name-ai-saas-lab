"""
Memory heapq
heapq utilities
"""
import heapq


def demo():
    heap = [3, 1, 2]
    heapq.heapify(heap)
    print(heapq.heappop(heap))


if __name__ == "__main__":
    demo()
