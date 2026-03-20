"""
Memory heapq_example11
heapq_example11
"""
import heapq


def demo():
    data = [5, 2, 8, 1, 9, 3]
    heapq.heapify(data)
    largest = heapq.nlargest(3, data)
    print(largest)


if __name__ == "__main__":
    demo()
