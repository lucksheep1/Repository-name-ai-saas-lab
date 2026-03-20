"""
Memory heapq_example8
heapq_example8
"""
import heapq


def demo():
    heap = [5, 3, 7, 1, 9]
    heapq.heapify(heap)
    largest = heapq.heappop(heap)
    print(largest)


if __name__ == "__main__":
    demo()
