"""
Memory heapq_example4
heapq_example4
"""
import heapq


def demo():
    heap = []
    heapq.heappush(heap, (1, "task1"))
    heapq.heappush(heap, (2, "task2"))
    priority, task = heapq.heappop(heap)
    print(priority, task)


if __name__ == "__main__":
    demo()
