"""
Memory heapq_example12
heapq_example12
"""
import heapq


def demo():
    heap = [3, 1, 4, 1, 5, 9, 2, 6]
    heapq.heapify(heap)
    smallest = heapq.heappop(heap)
    print(f"Smallest: {smallest}, heap: {heap}")


if __name__ == "__main__":
    demo()
