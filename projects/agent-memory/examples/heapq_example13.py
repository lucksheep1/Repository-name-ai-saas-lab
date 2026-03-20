"""
Memory heapq_example13
heapq_example13
"""
import heapq


def demo():
    heap = [5, 2, 8, 1, 9]
    heapq.heapify(heap)
    smallest = heapq.heappop(heap)
    print(smallest)


if __name__ == "__main__":
    demo()
