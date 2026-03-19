"""
Memory heapq_example2
heapq_example2
"""
import heapq


def demo():
    heap = []
    heapq.heappush(heap, 5)
    heapq.heappush(heap, 1)
    heapq.heappush(heap, 3)
    print(heapq.heappop(heap))


if __name__ == "__main__":
    demo()
