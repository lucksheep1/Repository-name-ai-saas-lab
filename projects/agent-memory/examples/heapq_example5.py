"""
Memory heapq_example5
heapq_example5
"""
import heapq


def demo():
    heap = [5, 2, 8, 1, 9]
    heapq.heapify(heap)
    smallest = heapq.nsmallest(3, heap)
    print(smallest)


if __name__ == "__main__":
    demo()
