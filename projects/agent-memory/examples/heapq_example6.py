"""
Memory heapq_example6
heapq_example6
"""
import heapq


def demo():
    heap = [5, 2, 8, 1, 9]
    heapq.heapify(heap)
    largest = heapq.heappop(heap)
    print(largest)


if __name__ == "__main__":
    demo()
